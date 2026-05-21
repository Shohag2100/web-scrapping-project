from datetime import timedelta
import random

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import OTP


def generate_otp_code():
    return f"{random.randint(0, 999999):06d}"


def create_otp(user, purpose):
    OTP.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)

    otp_code = generate_otp_code()
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    otp_obj = OTP.objects.create(user=user, code=otp_code, purpose=purpose, expires_at=expires_at)
    return otp_obj


def send_otp_email(user, otp_obj, subject):
    message = (
        f"Hello {user.full_name or user.email},\n\n"
        f"Your verification code is: {otp_obj.code}\n"
        f"It will expire at {otp_obj.expires_at:%Y-%m-%d %H:%M:%S} UTC.\n\n"
        "If you did not request this code, you can ignore this email."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
