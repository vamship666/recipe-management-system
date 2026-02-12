"""
Django settings for recipe_project project.
"""

from pathlib import Path
import os

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY SETTINGS
# ------------------------------------------------------------------

# Secret key (should be kept secure in production)
SECRET_KEY = 'django-insecure-a35b=ac14=#@k%c4!n#l0k^d5tjz6=lynri_-#d)*dt%0*59*o'

# Enable debug mode (disable in production)
DEBUG = True

# Allowed hosts (configure in production)
ALLOWED_HOSTS = []


# APPLICATIONS
# ------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'django_filters',

    # Local apps
    'accounts',
    'recipes',
    'favorites',
    'utils',
]


# MIDDLEWARE
# ------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'recipe_project.urls'


# TEMPLATES CONFIGURATION
# ------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'recipe_project.wsgi.application'


# DATABASE CONFIGURATION
# ------------------------------------------------------------------

# PostgreSQL database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recipe_db',
        'USER': 'postgres',
        'PASSWORD': 'Vaanara',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# PASSWORD VALIDATION
# ------------------------------------------------------------------

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


# INTERNATIONALIZATION
# ------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# STATIC & MEDIA FILES
# ------------------------------------------------------------------

STATIC_URL = 'static/'

# Media files (uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# CUSTOM USER MODEL
# ------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"


# DJANGO REST FRAMEWORK SETTINGS
# ------------------------------------------------------------------

REST_FRAMEWORK = {
    # Token-based authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],

    # Require authentication by default
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    # Pagination configuration
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,

    # Swagger / OpenAPI schema generation
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    # Enable filtering, searching, and ordering globally
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}


# SWAGGER / API DOCUMENTATION SETTINGS
# ------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
    "TITLE": "Recipe Management API",
    "DESCRIPTION": "API for managing recipes with creators and viewers",
    "VERSION": "1.0.0",
}


# DEFAULT PRIMARY KEY TYPE
# ------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
