
from django.conf import settings
from celery import shared_task
from .models import Borrowing
from django.core.mail import send_mail



@shared_task
def send_admin_borrowing_mail(instance_id):
    instance = Borrowing.objects.get(id= instance_id)
    send_mail(
        'New Book Borrowing',
        f'Customer {instance.user.username} borrowed {instance.book.title}. End date: {instance.end_date}',
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
        )
    

@shared_task
def send_borrowing_reminder():
    from django.utils import timezone
    from datetime import timedelta
    current_date = timezone.now().date()
    threshold_date = current_date + timedelta(days=5)
    instances = Borrowing.objects.filter(
    end_date__lte=threshold_date,
    end_date__gte=current_date,
    returned=False)
    for instance in instances:
        days_left = (instance.end_date - current_date).days
        send_mail(
            subject='Library Book Return Reminder',
            message=(
                f"Dear {instance.user.username},\n\n"
                f"This is a reminder that you borrowed '{instance.book.title}' by {instance.book.author}.\n"
                f"The borrowing period ends on {instance.end_date} ({days_left} days remaining).\n\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=False,
        )
