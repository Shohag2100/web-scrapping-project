# How To Run And Use This Scrapping Project

This guide explains how this Django project works and how to use the scraping API end to end.

## 1) What this project does

- Project: `core`
- Auth app: `account`
  - Email registration, email verification, JWT login, password reset, change password, and profile picture support with 6-digit OTP
- Scraping app: `scraped`
  - Authenticated users can scrape website data and view their own scrape history

## 2) Prerequisites

- Python 3.10+
- PostgreSQL running locally (or remote)
- Database credentials configured in `.env`

## 3) Environment setup

1. Create/activate virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure `.env` file in project root:

```env
SECRET_KEY=django-insecure-change-this-key
DEBUG=True
ALLOWED_HOSTS=*

DB_ENGINE=django.db.backends.postgresql
DB_NAME=scrapping_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

OTP_EXPIRE_MINUTES=5
JWT_ACCESS_MINUTES=30
JWT_REFRESH_DAYS=7

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

## 4) Run migrations and start server

```bash
python manage.py migrate
python manage.py runserver
```

Server default URL:
- `http://127.0.0.1:8000`

## 5) API flow (important)

Use APIs in this order:

1. Register with email and password
2. Verify the email OTP to get JWT token
3. Log in with email and password
4. Use JWT token to change password, update profile, or scrape a URL
5. Get scraping history

## 6) API endpoints

### A) Register

- Method: `POST`
- URL: `/api/account/register/`
- Body:

```json
{
  "full_name": "Shohag",
  "email": "you@example.com",
  "password": "Password123",
  "confirm_password": "Password123"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/account/register/ \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Shohag","email":"you@example.com","password":"Password123","confirm_password":"Password123"}'
```

Note:
- In `DEBUG=True`, response includes the OTP for testing.

### B) Verify email and get JWT token

- Method: `POST`
- URL: `/api/account/verify-email/`
- Body:

```json
{
  "email": "you@example.com",
  "otp": "123456"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/account/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","otp":"123456"}'
```

Response contains:
- `access` token
- `refresh` token
- user info

Save the `access` token for next requests.

### C) Login

- Method: `POST`
- URL: `/api/account/login/`
- Body:

```json
{
  "email": "you@example.com",
  "password": "Password123"
}
```

### D) Change password

- Method: `POST`
- URL: `/api/account/change-password/`
- Header: `Authorization: Bearer <access_token>`
- Body:

```json
{
  "old_password": "Password123",
  "new_password": "NewPass123",
  "confirm_new_password": "NewPass123"
}
```

### E) Forgot password

1. Request OTP:

- Method: `POST`
- URL: `/api/account/forgot-password/request/`
- Body:

```json
{
  "email": "you@example.com"
}
```

2. Confirm reset:

- Method: `POST`
- URL: `/api/account/forgot-password/confirm/`
- Body:

```json
{
  "email": "you@example.com",
  "otp": "123456",
  "new_password": "NewPass123",
  "confirm_new_password": "NewPass123"
}
```

### F) Scrape a website

- Method: `POST`
- URL: `/api/scraped/run/`
- Header: `Authorization: Bearer <access_token>`
- Body:

```json
{
  "url": "https://example.com"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/scraped/run/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"url":"https://example.com"}'
```

It returns scraped data like:
- `title`
- `meta_description`
- `h1_tags`
- `links_count`
- `text_length`

### G) Get your scraping history

- Method: `GET`
- URL: `/api/scraped/history/`
- Header: `Authorization: Bearer <access_token>`

Example:

```bash
curl -X GET http://127.0.0.1:8000/api/scraped/history/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### H) Refresh token

- Method: `POST`
- URL: `/api/account/token/refresh/`
- Body:

```json
{
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

## 7) Optional: test user profile endpoint

```bash
curl -X GET http://127.0.0.1:8000/api/account/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Update profile picture or name:

```bash
curl -X PATCH http://127.0.0.1:8000/api/account/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "full_name=New Name" \
  -F "profile_picture=@/path/to/photo.jpg"
```

## 8) Common issues and fixes

1. `password authentication failed for user postgres`
- Fix DB credentials in `.env` (`DB_USER`, `DB_PASSWORD`).

2. `connection refused 127.0.0.1:5432`
- PostgreSQL is not running. Start PostgreSQL service.

3. OTP always invalid
- Request OTP again and verify within `OTP_EXPIRE_MINUTES`.

4. `401 Unauthorized` on scrape endpoints
- Missing/expired access token. Verify OTP again or refresh token.

5. `Import "dotenv" could not be resolved`
- Make sure VS Code uses the `env` interpreter and that `python-dotenv` is installed there.

## 9) Quick command summary

```bash
source env/bin/activate
python manage.py migrate
python manage.py runserver
```

Then use endpoints in this exact flow:
- `/api/account/request-otp/`
- `/api/account/verify-otp/`
- `/api/scraped/run/`
- `/api/scraped/history/`
