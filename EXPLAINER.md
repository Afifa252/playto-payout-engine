# 💡 Payout Engine – Explainer

## 📌 Overview
This project is a backend payout processing system built using Django and Django REST Framework. It allows users to create payout requests via an API endpoint and processes them asynchronously using Celery and Redis.

The goal of this project is to simulate a real-world payout system where tasks are handled in the background for scalability and performance.

---

## ⚙️ Architecture

Client (Postman / API Call)
        ↓
Django REST API
        ↓
Celery Task Queue
        ↓
Redis (Broker)
        ↓
Background Worker (Celery)
        ↓
Payout Processing Logic

---

## 🚀 Features

- Create payout via REST API
- Asynchronous processing using Celery
- Redis as message broker
- Scalable backend design
- Deployed on Render

---

## 🌐 Live API

Base URL:
https://playto-payout-engine1.onrender.com/

### Endpoint:
POST `/api/v1/payouts/`

---

## 🧪 Example Request

```json
{
  "amount": 1000,
  "currency": "INR",
  "recipient": "test_user"
}
