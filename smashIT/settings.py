from pathlib import Path
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = ["*"]

SITE_ID = 9


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'convert.apps.ConvertConfig',
    'django.contrib.sitemaps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github', 

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'smashIT.urls'


WSGI_APPLICATION = 'smashIT.wsgi.application'


# Add these at the top of your settings.py


# Replace the DATABASES section of your settings.py with this
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
# Check if a custom port is set
RUNSERVER_PORT = 8000  # Default port is usually 8000


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = 'static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'convert/static'),
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

STATIC_ROOT = BASE_DIR / 'static'  
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OCR_API_KEY =  os.getenv("OCR_API_KEY")
AUTH0_CLIENT_ID= os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET= os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN= os.getenv("AUTH0_DOMAIN")



STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "convert", "static"),  # App-level static files
]

# This should be different from STATICFILES_DIRS to avoid duplication
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Collects all static files during deployment

STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

# Media Files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_METHODS = {'email'}  # or {'email'} or {'username', 'email'}
ACCOUNT_EMAIL_REQUIRED = True  # Set to False if email login is not needed
ACCOUNT_USERNAME_REQUIRED = False  # Set to False if username login is not needed
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_REQUIRED = True

LOGIN = '/login'

SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

SOCIALACCOUNT_LOGIN_ON_GET=True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,  # PKCE improves security
    },
    'github': {
         "SCOPE": [
            "read:user",  
            "user:email",  
        ],
        "AUTH_PARAMS": {
            "allow_signup": "true",
        },
    },
}

CSRF_TRUSTED_ORIGINS = [
    "https://smash-it-peach.vercel.app",  
    "http://smash-it-peach.vercel.app",  
    "https://qpaper.live",  
    "http://qpaper.live",  
    "https://smashit.onrender.com",
    "http://smashit.onrender.com",
    "http://www.smashit.onrender.com",
    "https://www.qpaper.live",
    "http://www.qpaper.live",
    "https://www.smashit.onrender.com",
]


SOCIALACCOUNT_ADAPTER = "convert.adapters.CustomSocialAccountAdapter"

AUTH_USER_MODEL = 'convert.CustomUser'

#production
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

IS_PRODUCTION = os.getenv("DJANGO_PRODUCTION", "true").lower() == "true"
if (not IS_PRODUCTION):
    DEBUG = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https" if IS_PRODUCTION else "http"
SECURE_SSL_REDIRECT = IS_PRODUCTION
CSRF_COOKIE_SECURE = IS_PRODUCTION
SESSION_COOKIE_SECURE = IS_PRODUCTION
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if IS_PRODUCTION else None