from celery import shared_task
from payouts.models import Payout, LedgerEntry
from django.db import transaction
import random


VALID_TRANSITIONS = {
    "pending": ["processing"],
    "processing": ["completed", "failed"]
}


def is_valid_transition(old, new):
    return new in VALID_TRANSITIONS.get(old, [])


@shared_task
def process_payout(payout_id):
    try:
        payout = Payout.objects.get(id=payout_id)

        if payout.status != "pending":
            return

        with transaction.atomic():

            if not is_valid_transition(payout.status, "processing"):
                return

            payout.status = "processing"
            payout.save()

            result = random.random()

            if result < 0.7:
                # SUCCESS
                if not is_valid_transition("processing", "completed"):
                    return

                payout.status = "completed"

                LedgerEntry.objects.create(
                    merchant=payout.merchant,
                    entry_type="debit",
                    amount_paise=payout.amount_paise,
                    reference_id=payout.id
                )

            else:
                # FAILURE
                if not is_valid_transition("processing", "failed"):
                    return

                payout.status = "failed"

                LedgerEntry.objects.create(
                    merchant=payout.merchant,
                    entry_type="release",
                    amount_paise=payout.amount_paise,
                    reference_id=payout.id
                )

            payout.save()

    except Exception as e:
        print("❌ Celery Error:", str(e))