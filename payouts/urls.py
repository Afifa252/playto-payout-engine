from django.urls import path
from .views import create_payout, get_payout, get_balance_api

urlpatterns = [
    path("payouts/", create_payout),
    path("payouts/<uuid:payout_id>/", get_payout),
    path("balance/", get_balance_api),
]