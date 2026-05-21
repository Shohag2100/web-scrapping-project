from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractUser):
	username = None
	email = models.EmailField(unique=True)
	full_name = models.CharField(max_length=255, blank=True)
	profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
	is_email_verified = models.BooleanField(default=False)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email


class OTP(models.Model):
	class Purpose(models.TextChoices):
		EMAIL_VERIFICATION = "email_verification", "Email Verification"
		PASSWORD_RESET = "password_reset", "Password Reset"

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
	code = models.CharField(max_length=6)
	purpose = models.CharField(max_length=32, choices=Purpose.choices)
	is_used = models.BooleanField(default=False)
	expires_at = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
		indexes = [models.Index(fields=["user", "purpose", "is_used"])]

	@property
	def is_expired(self):
		return timezone.now() > self.expires_at

	def __str__(self):
		return f"{self.user.email} - {self.purpose} - {self.code}"
