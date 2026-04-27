web: gunicorn playto_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2
worker: celery -A playto_backend worker -l info