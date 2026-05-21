# Core Scrapping Project

Django REST API project with:
- Project name: `core`
- App `account`: email registration, email verification, JWT login, password reset, and profile management with 6-digit OTP
- App `scraped`: website scraping APIs for authenticated users

## Setup

1. Activate virtual environment (folder name: `env`):

```bash
source env/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`.

PostgreSQL variables:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=scrapping_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

Email variables:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USER=your_email@gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
```
```

4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run server:

```bash
python manage.py runserver
```

## API Endpoints

### Account
- `POST /api/account/register/`
  - Body: `{ "full_name": "Your Name", "email": "you@example.com", "password": "Password123", "confirm_password": "Password123" }`
- `POST /api/account/verify-email/`
  - Body: `{ "email": "you@example.com", "otp": "123456" }`
- `POST /api/account/login/`
  - Body: `{ "email": "you@example.com", "password": "Password123" }`
- `POST /api/account/change-password/`
  - Body: `{ "old_password": "OldPass123", "new_password": "NewPass123", "confirm_new_password": "NewPass123" }`
- `POST /api/account/forgot-password/request/`
  - Body: `{ "email": "you@example.com" }`
- `POST /api/account/forgot-password/confirm/`
  - Body: `{ "email": "you@example.com", "otp": "123456", "new_password": "NewPass123", "confirm_new_password": "NewPass123" }`
- `POST /api/account/token/refresh/`
- `GET /api/account/profile/` (Bearer token required)
- `PUT /api/account/profile/` (Bearer token required)
- `PATCH /api/account/profile/` (Bearer token required)

### Scraping
- `POST /api/scraped/run/` (Bearer token required)
  - Body: `{ "url": "https://example.com" }`
- `GET /api/scraped/history/` (Bearer token required)

## Notes
- In DEBUG mode, registration and password-reset responses include the generated OTP for development/testing.
- OTP expires based on `OTP_EXPIRE_MINUTES`.
- Profile picture uploads use `MEDIA_ROOT=/media/` in development.
