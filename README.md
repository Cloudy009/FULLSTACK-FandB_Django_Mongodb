# FandB-Mongodb-Django

This project is a web-based Food & Beverage (F&B) management system developed using Django and MongoDB. It provides core functionalities for managing menu items, orders, and users within a modern admin interface.

## Features

- ✅ Django + MongoDB integration (`djongo`)
- ✅ Admin dashboard using [Soft UI Dashboard](https://appseed.us/product/soft-ui-dashboard/django/) by AppSeed
- ✅ Role-based access (staff/admin)
- ✅ Product and category management
- ✅ Order tracking and payment integration (VNPAY)
- ✅ Google & GitHub OAuth login
- ✅ Email notifications

---

## 🔧 Local Setup

### 1. Clone the project

```bash
git clone https://github.com/yourusername/FandB-Mongodb-django.git
cd FandB-Mongodb-django
```

### 2. Create and activate virtual environment
# Create virtual environment
```bash
python -m venv venv_django_mongo
```

# Activate (choose OS)
# On Windows:
```bash
.\venv_django_mongo\Scripts\activate
```
# On macOS/Linux:
```bash
source venv_django_mongo/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. MongoDB configuration
Create a MongoDB database named FandBShop
Update the following section in settings.py:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'FandBShop',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
        },
    }
}
```

### 5. Configure .env file
Create a .env file in the root directory and add:

```bash
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://localhost:27017

# Google OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-secret
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=http://127.0.0.1:8000/social-auth/complete/google-oauth2/

# GitHub OAuth
SOCIAL_AUTH_GITHUB_KEY=your-github-key
SOCIAL_AUTH_GITHUB_SECRET=your-github-secret
SOCIAL_AUTH_GITHUB_REDIRECT_URI=http://127.0.0.1:8000/social-auth/complete/github/

# Email config
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
DEFAULT_TO_EMAIL=your-email@gmail.com

# VNPAY Payment
VNPAY_RETURN_URL=http://localhost:8000/shop/payment_return
VNPAY_PAYMENT_URL=https://sandbox.vnpayment.vn/paymentv2/vpcpay.html
VNPAY_API_URL=https://sandbox.vnpayment.vn/merchant_webapi/api/transaction
VNPAY_TMN_CODE=your-vnpay-tmn-code
VNPAY_HASH_SECRET_KEY=your-vnpay-secret-key

DEBUG=True
```

### 6. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate

# Fake social_django migrations if needed
python manage.py migrate social_django 0010 --fake
python manage.py migrate social_django 0011 --fake
python manage.py migrate social_django 0012 --fake

python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```
Follow the prompt to set up the admin credentials.

### 8. Start development server
```bash
python manage.py runserver
```
Open in browser: http://127.0.0.1:8000

🧩 Admin Dashboard (AppSeed)
This project uses the open-source Django Soft UI Dashboard by AppSeed:
Responsive UI built with Bootstrap 5
Reusable components and modern styling
Includes login, register, and dashboard pages

🔗 Live Demo: [link] (https://django-soft-dash.onrender.com/)

📁 Project Structure
fandb/
│
├── core/               # Django settings and config
├── menu/               # F&B app models, views, urls
├── templates/          # HTML templates (Soft UI)
├── static/             # CSS, JS, images
├── .env                # Environment variables
├── manage.py
└── requirements.txt

📦 Dependencies
- Django
- Djongo (MongoDB connector for Django)
- social-auth-app-django
- python-decouple
- requests, django-crispy-forms, etc.