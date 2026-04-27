from django.db import models
from payouts.models import LedgerEntry


def get_balance(merchant):
    """
    balance = credits - debits - holds + releases
    """

    credits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type="credit"
    ).aggregate(total=models.Sum("amount_paise"))["total"] or 0

    debits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type="debit"
    ).aggregate(total=models.Sum("amount_paise"))["total"] or 0

    holds = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type="hold"
    ).aggregate(total=models.Sum("amount_paise"))["total"] or 0

    releases = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type="release"
    ).aggregate(total=models.Sum("amount_paise"))["total"] or 0

    return credits - debits - holds + releases