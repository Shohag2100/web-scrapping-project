from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP, User
from .serializers import (
	ChangePasswordSerializer,
	ForgotPasswordConfirmSerializer,
	ForgotPasswordRequestSerializer,
	LoginSerializer,
	ProfileSerializer,
	RegisterSerializer,
	VerifyEmailSerializer,
)
from .services import create_otp, send_otp_email


def get_tokens_for_user(user):
	refresh = RefreshToken.for_user(user)
	return {
		"access": str(refresh.access_token),
		"refresh": str(refresh),
	}


class RegisterView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		full_name = serializer.validated_data["full_name"]
		email = serializer.validated_data["email"].lower()
		password = serializer.validated_data["password"]
		confirm_password = serializer.validated_data["confirm_password"]

		if password != confirm_password:
			return Response({"detail": "Password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

		user = User.objects.filter(email=email).first()
		if user and user.is_email_verified:
			return Response({"detail": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

		if user is None:
			user = User.objects.create_user(email=email, password=password, full_name=full_name)
		else:
			user.full_name = full_name
			user.set_password(password)
			user.save(update_fields=["full_name", "password"])

		user.is_email_verified = False
		user.save(update_fields=["is_email_verified"])

		otp_obj = create_otp(user, OTP.Purpose.EMAIL_VERIFICATION)
		send_otp_email(user, otp_obj, "Verify your email address")

		response_data = {
			"message": "Registration successful. Verification OTP sent to email.",
			"email": user.email,
			"expires_at": otp_obj.expires_at,
		}
		if settings.DEBUG:
			response_data["otp"] = otp_obj.code

		return Response(response_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = VerifyEmailSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		email = serializer.validated_data["email"].lower()
		otp_code = serializer.validated_data["otp"]

		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

		otp_obj = OTP.objects.filter(
			user=user,
			code=otp_code,
			purpose=OTP.Purpose.EMAIL_VERIFICATION,
			is_used=False,
		).order_by("-created_at").first()
		if not otp_obj:
			return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

		if otp_obj.expires_at < timezone.now():
			return Response({"detail": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

		otp_obj.is_used = True
		otp_obj.save(update_fields=["is_used"])
		user.is_email_verified = True
		user.save(update_fields=["is_email_verified"])

		tokens = get_tokens_for_user(user)
		return Response({**tokens, "user": ProfileSerializer(user).data}, status=status.HTTP_200_OK)


class LoginView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		email = serializer.validated_data["email"].lower()
		password = serializer.validated_data["password"]

		user = authenticate(request, username=email, password=password)
		if not user:
			return Response({"detail": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
		if not user.is_email_verified:
			return Response({"detail": "Please verify your email first"}, status=status.HTTP_400_BAD_REQUEST)

		tokens = get_tokens_for_user(user)
		return Response({**tokens, "user": ProfileSerializer(user).data}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		serializer = ChangePasswordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		old_password = serializer.validated_data["old_password"]
		new_password = serializer.validated_data["new_password"]
		confirm_new_password = serializer.validated_data["confirm_new_password"]

		if new_password != confirm_new_password:
			return Response({"detail": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)
		if not request.user.check_password(old_password):
			return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

		request.user.set_password(new_password)
		request.user.save(update_fields=["password"])
		return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)


class ForgotPasswordRequestView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = ForgotPasswordRequestSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		email = serializer.validated_data["email"].lower()
		user = User.objects.filter(email=email).first()
		if user:
			otp_obj = create_otp(user, OTP.Purpose.PASSWORD_RESET)
			send_otp_email(user, otp_obj, "Reset your password")
			if settings.DEBUG:
				return Response({"message": "Password reset OTP sent to email.", "otp": otp_obj.code}, status=status.HTTP_200_OK)

		return Response({"message": "Password reset OTP sent to email."}, status=status.HTTP_200_OK)


class ForgotPasswordConfirmView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = ForgotPasswordConfirmSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		email = serializer.validated_data["email"].lower()
		otp_code = serializer.validated_data["otp"]
		new_password = serializer.validated_data["new_password"]
		confirm_new_password = serializer.validated_data["confirm_new_password"]

		if new_password != confirm_new_password:
			return Response({"detail": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

		otp_obj = OTP.objects.filter(
			user=user,
			code=otp_code,
			purpose=OTP.Purpose.PASSWORD_RESET,
			is_used=False,
		).order_by("-created_at").first()
		if not otp_obj:
			return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

		if otp_obj.expires_at < timezone.now():
			return Response({"detail": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

		otp_obj.is_used = True
		otp_obj.save(update_fields=["is_used"])
		user.set_password(new_password)
		user.save(update_fields=["password"])
		return Response({"detail": "Password reset successfully"}, status=status.HTTP_200_OK)


class ProfileView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		serializer = ProfileSerializer(request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def put(self, request):
		serializer = ProfileSerializer(request.user, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

	def patch(self, request):
		serializer = ProfileSerializer(request.user, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
