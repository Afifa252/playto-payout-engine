import uuid
from django.db import models


class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LedgerEntry(models.Model):
    ENTRY_TYPES = [
        ("credit", "Credit"),
        ("debit", "Debit"),
        ("hold", "Hold"),
        ("release", "Release"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ✅ Add index for performance
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        db_index=True
    )

    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    amount_paise = models.BigIntegerField()

    # ✅ FIXED: optional reference (correct design)
    reference_id = models.UUIDField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # ✅ latest first

    def __str__(self):
        return f"{self.entry_type} - {self.amount_paise}"


class Payout(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ✅ index for faster queries
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        db_index=True
    )

    amount_paise = models.BigIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # ✅ default added (good)
    bank_account_id = models.CharField(max_length=255, default="test_bank")

    retry_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} - {self.status}"


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255)

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        db_index=True
    )

    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("key", "merchant")
        ordering = ["-created_at"]

    def __str__(self):
        return self.key