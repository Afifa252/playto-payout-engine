# 💸 Payout API (Django + DRF + Celery)

## 🚀 Overview
This project is a backend API for creating payouts.  
Built using Django REST Framework with async processing using Celery and Redis.

---

## 🌐 Live Deployment
👉 https://playto-payout-engine1.onrender.com/

---

## 📌 API Endpoint

### Create Payout
POST `/api/v1/payouts/`

### Sample Request
```json
{
  "amount": 1000,
  "currency": "INR",
  "recipient": "test_user"
}
⚠️ Notes


Only POST method is allowed


GET will return:


Method "GET" not allowed

🧪 Testing (Postman)
POST →
https://playto-payout-engine1.onrender.com/api/v1/payouts/
Body:
{  "amount": 1000,  "currency": "INR",  "recipient": "test_user"}

⚙️ Tech Stack


Django


Django REST Framework


Celery


Redis


Render



👩‍💻 Author
Afifa Khanum
