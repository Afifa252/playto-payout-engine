from django.core.management.base import BaseCommand
from payouts.models import Merchant, LedgerEntry


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        merchant = Merchant.objects.create(name="Demo Merchant")

        LedgerEntry.objects.create(
            merchant=merchant,
            entry_type="credit",
            amount_paise=100000
        )

        self.stdout.write("✅ Seed data created")