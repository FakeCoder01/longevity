from django.contrib.auth.models import User
from django.core.mail import send_mail
from celery import shared_task
     
@shared_task
def send_otp_email(user_email, otp):
    try:
        message = f"Your OTP for the login is : {otp}"
        send_mail(
            f'OTP Verification : {otp}',
            message,
            'asamajder836@gmail.com',
            [user_email],
            fail_silently=False,
        )
    except:
        pass

