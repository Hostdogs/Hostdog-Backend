web: gunicorn backend.wsgi:application --log-file -
release: python manage.py migrate
worker: celery -A backend worker -l info --pool=solo
beat: celery -A backend beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler