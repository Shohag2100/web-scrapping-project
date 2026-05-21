from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import OTP, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	model = User
	list_display = ("id", "email", "full_name", "is_email_verified", "is_staff", "is_active", "date_joined")
	list_filter = ("is_staff", "is_superuser", "is_active")
	ordering = ("-date_joined",)
	search_fields = ("email", "full_name")

	fieldsets = (
		(None, {"fields": ("email", "password")}),
		("Personal info", {"fields": ("full_name", "profile_picture")}),
		(
			"Permissions",
			{
				"fields": (
					"is_email_verified",
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				)
			},
		),
		("Important dates", {"fields": ("last_login", "date_joined")}),
	)
	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("email", "full_name", "password1", "password2"),
			},
		),
	)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "purpose", "code", "is_used", "expires_at", "created_at")
	list_filter = ("is_used",)
	search_fields = ("user__email", "code")
