# 🚀 Payout Processing System (Django + Celery)

## 📌 Overview

This project simulates a real-world payout system similar to Razorpay/Stripe.

It ensures:

* Idempotent payout requests
* Safe balance handling
* Async processing with Celery
* Retry mechanism for failures

---

## 🧠 System Design

### 1. Ledger-Based Accounting

Instead of storing balance directly, we maintain a ledger.

Each transaction is recorded as:

* credit → add money
* debit → deduct money
* hold → reserve money for payout
* release → refund failed payout

Balance is calculated dynamically:

```
balance = credits - (debits + holds)
```

---

### 2. Idempotency Handling

Each payout request uses an Idempotency-Key.

If the same request is sent twice:

* The system returns the same response
* Prevents duplicate payouts

---

### 3. Concurrency Handling

We use:

```
select_for_update()
```

This locks the merchant row to avoid:

* double spending
* race conditions

---

### 4. Async Processing (Celery)

Payout processing is handled asynchronously.

Flow:

1. API creates payout (status = pending)
2. Celery worker picks task
3. Status changes:

   * pending → processing → completed/failed

---

### 5. Retry Logic

If payout fails:

* retry_count is incremented
* retried up to 3 times

---

## 🔄 Payout Flow

1. User sends POST request
2. System checks balance
3. HOLD entry created
4. Celery task triggered
5. Worker processes payout:

   * success → debit entry
   * failure → release entry

---

## ⚠️ Failure Handling

If payout fails:

* Amount is released
* Balance is restored
* Retry mechanism kicks in

---

## 🧪 API Endpoints

### Create Payout

POST /api/v1/payouts/

### Get Payout Status

GET /api/v1/payouts/{id}/

---

## 🛠 Tech Stack

* Django (Backend)
* PostgreSQL (Database)
* Redis (Broker)
* Celery (Async tasks)

---

## 📊 Key Highlights

* Prevents duplicate transactions
* Handles concurrency safely
* Maintains financial integrity
* Simulates real fintech system

---

## 🚀 Future Improvements

* Webhooks for payout updates
* Authentication system
* Multi-merchant support
* Admin dashboard

---
