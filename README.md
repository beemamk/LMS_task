# LMS_task
Simple library management system API using Django REST framework, and scheduled reminder email using celery beat and redis

Requirements

Python 3.10+
Django 4.x/5.x
Django REST Framework
Redis (for Celery)
SQLite (default database)

Installation


Install dependencies:pip install -r requirements.txt


Run migrations:python manage.py makemigrations accounts library
python manage.py migrate


Create a superuser:python manage.py createsuperuser


Start Redis server:redis-server


Run Django server:python manage.py runserver


Run Celery worker:celery -A config worker -l info


Run Celery Beat (for scheduled tasks):celery -A config beat -l info

