"""
Django settings for nederlearn project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
<https://docs.djangoproject.com/en/4.2/topics/settings/>

For the full list of settings and their values, see
<https://docs.djangoproject.com/en/4.2/ref/settings/>
"""

# ---------------------
# Standard library imports
# ---------------------
from pathlib import Path
import os
import dj_database_url

if os.path.isfile("env.py"):
    import env

# ---------------------
# Build paths inside the project
# ---------------------
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# ---------------------
# Quick-start development settings - unsuitable for production
# See <https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/>
# ---------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")  

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "8000-blignaut24-nederlearnv2-5ijo1es0adm.ws.codeinstitute-ide.net",
    ".herokuapp.com",
]
# ---------------------
# Application definition
# ---------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
    'cloudinary',
    'django_summernote',
    'blog',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'nederlearn.urls'

# ---------------------
# Templates Definition
# ---------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'nederlearn.wsgi.application'

# ---------------------
# Database
# Some sections are commented out right now, but we're keeping them
# for later. They're like a guide we can use when we need. This includes
# the Database section. If you want more details, check out Django's
# database guide. If we need this section for work we're doing locally,
# we can start using it again.
# <https://docs.djangoproject.com/en/4.2/ref/settings/#databases>
# ---------------------

# Set up the production database using dj-database-url.
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# TEMPORARY TEST SECTION
"""
This part is about setting up the database for tests.
Keep it off unless you're doing local tests or running
a CI/CD pipeline. It's very important to keep this part
off in a real work setting to avoid changes to the real
database settings by mistake.
"""

# ---------------------
# Password validation
# <https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators>
# ---------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# ---------------------
# Internationalization
# <https://docs.djangoproject.com/en/3.2/topics/i18n/>
# ---------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ---------------------
# Static files (CSS, JavaScript, Images)
# <https://docs.djangoproject.com/en/3.2/howto/static-files/>
# ---------------------
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ---------------------
# Default primary key field type
# <https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field>
# ----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_VERIFICATION = 'none'
