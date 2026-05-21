import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from rest_framework.test import APIClient
from account.models import OTP, User

def run_test():
    client = APIClient()
    phone = "01700000000"
    
    # 1. Request OTP
    print("Requesting OTP...")
    req_otp_res = client.post('/api/account/request-otp/', {'phone': phone}, format='json')
    print(f"Request OTP Response: {req_otp_res.status_code} {req_otp_res.data}")
    
    # 2. Read OTP from DB
    try:
    from account.models import OTP, User
        otp_obj = OTP.objects.filter(user=user).latest('created_at')
        otp_code = otp_obj.code
        print(f"Retrieved OTP: {otp_code}")
        email = "shohag.test@example.com"
        password = "Password123"
        print(f"Error retrieving OTP: {e}")
        # 1. Register
        print("Registering user...")
        register_res = client.post(
            '/api/account/register/',
            {
                'full_name': 'Shohag Test',
                'email': email,
                'password': password,
                'confirm_password': password,
            },
            format='json'
        )
        print(f"Register Response: {register_res.status_code} {register_res.data}")
    verify_res = client.post('/api/account/verify-otp/', {'phone': phone, 'otp': otp_code}, format='json')
        # 2. Read OTP from DB
        user = User.objects.get(email=email)
        otp_obj = OTP.objects.filter(user=user, purpose=OTP.Purpose.EMAIL_VERIFICATION).latest('created_at')
        otp_code = otp_obj.code
    access_token = None
    if isinstance(data, dict):
        # 3. Verify email
        print("Verifying email...")
        verify_res = client.post('/api/account/verify-email/', {'email': email, 'otp': otp_code}, format='json')
        print(f"Verify Email Response: {verify_res.status_code} {verify_res.data}")
    if not access_token:
        print(f"Failed to get access token from response: {data}")
        return

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        # 4. Login
        login_res = client.post('/api/account/login/', {'email': email, 'password': password}, format='json')
        print(f"Login Response: {login_res.status_code} {login_res.data}")
    
        # 5. Change password
        change_res = client.post('/api/account/change-password/', {
            'old_password': password,
            'new_password': 'NewPass123',
            'confirm_new_password': 'NewPass123',
        }, format='json')
        print(f"Change Password Response: {change_res.status_code} {change_res.data}")

        # 6. Profile get/patch
        profile_get = client.get('/api/account/profile/')
        print(f"Profile GET Response: {profile_get.status_code} {profile_get.data}")

        profile_patch = client.patch('/api/account/profile/', {'full_name': 'Shohag Updated'}, format='json')
        print(f"Profile PATCH Response: {profile_patch.status_code} {profile_patch.data}")

        # 7. Scrape run
    print("Running Scrape...")
    scrape_res = client.post('/api/scraped/run/', {'url': 'https://example.com'}, format='json')
    print(f"Scrape Run Response: {scrape_res.status_code} {scrape_res.data}")
    
        # 8. Scrape history
    print("Checking History...")
    history_res = client.get('/api/scraped/history/')
    print(f"Scrape History Response: {history_res.status_code} {history_res.data}")

if __name__ == "__main__":
    run_test()
