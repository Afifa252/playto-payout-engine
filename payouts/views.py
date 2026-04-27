from payouts.tasks import process_payout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from payouts.models import Merchant, Payout, LedgerEntry, IdempotencyKey
from payouts.services import get_balance


# 🚀 CREATE PAYOUT API
@api_view(["POST"])
def create_payout(request):

    merchant = Merchant.objects.first()

    if not merchant:
        return Response({"error": "No merchant found"}, status=400)

    # ✅ Validate amount
    amount = request.data.get("amount_paise")

    if amount is None:
        return Response({"error": "amount_paise is required"}, status=400)

    try:
        amount = int(amount)
        if amount <= 0:
            return Response({"error": "amount must be greater than 0"}, status=400)
    except:
        return Response({"error": "amount must be integer"}, status=400)

    # ✅ Validate idempotency key
    idempotency_key = request.headers.get("Idempotency-Key")

    if not idempotency_key:
        return Response({"error": "Idempotency-Key header required"}, status=400)

    # ✅ Idempotency check (WITH 24hr expiry)
    existing = IdempotencyKey.objects.filter(
        key=idempotency_key,
        merchant=merchant,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).first()

    if existing:
        return Response(existing.response_data)

    with transaction.atomic():

        # 🔒 Lock merchant row (prevents race condition)
        merchant_locked = Merchant.objects.select_for_update().get(id=merchant.id)

        balance = get_balance(merchant_locked)

        print("DEBUG BALANCE:", balance)

        # ❌ Block insufficient balance
        if balance < amount:
            return Response(
                {"error": "Insufficient balance", "balance": balance},
                status=400
            )

        # ✅ Create payout
        payout = Payout.objects.create(
            merchant=merchant_locked,
            amount_paise=amount,
            status="pending",
            bank_account_id="test_bank"
        )

        # ✅ HOLD funds
        LedgerEntry.objects.create(
            merchant=merchant_locked,
            entry_type="hold",
            amount_paise=amount,
            reference_id=payout.id
        )

        # 🚀 Trigger async task
        process_payout.delay(str(payout.id))

        response_data = {
            "payout_id": str(payout.id),
            "status": payout.status
        }

        # ✅ Save idempotency response
        IdempotencyKey.objects.create(
            key=idempotency_key,
            merchant=merchant_locked,
            response_data=response_data
        )

    return Response(response_data)


# 📊 GET PAYOUT STATUS API
@api_view(["GET"])
def get_payout(request, payout_id):
    try:
        payout = Payout.objects.get(id=payout_id)

        return Response({
            "payout_id": str(payout.id),
            "status": payout.status,
            "amount_paise": payout.amount_paise,
            "merchant_id": str(payout.merchant.id)
        })

    except Payout.DoesNotExist:
        return Response({"error": "Payout not found"}, status=404)


# 💰 GET BALANCE API
@api_view(["GET"])
def get_balance_api(request):
    merchant = Merchant.objects.first()

    if not merchant:
        return Response({"error": "No merchant found"}, status=400)

    balance = get_balance(merchant)

    return Response({
        "merchant_id": str(merchant.id),
        "balance": balance
    })