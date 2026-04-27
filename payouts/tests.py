import uuid
from django.test import TestCase
from payouts.models import Merchant, LedgerEntry
from payouts.services import get_balance
from rest_framework.test import APIClient


class PayoutTests(TestCase):

    def setUp(self):
        self.merchant = Merchant.objects.create(name="Test Merchant")

        LedgerEntry.objects.create(
            merchant=self.merchant,
            entry_type="credit",
            amount_paise=10000
        )

        self.client = APIClient()

    def test_idempotency(self):
        key = str(uuid.uuid4())

        res1 = self.client.post(
            "/api/v1/payouts/",
            {"amount_paise": 1000},
            format="json",
            HTTP_Idempotency_Key=key
        )

        res2 = self.client.post(
            "/api/v1/payouts/",
            {"amount_paise": 1000},
            format="json",
            HTTP_Idempotency_Key=key
        )

        self.assertEqual(res1.data, res2.data)

    def test_balance_never_negative(self):
        balance = get_balance(self.merchant)
        self.assertTrue(balance >= 0)