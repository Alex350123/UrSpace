"""
Django settings for UrSpace project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 让 Django 识别静态文件
STATIC_URL = "/static/"

# 让 `collectstatic` 复制文件到这里
STATIC_ROOT = BASE_DIR / "staticfiles"

# **不要** 设置 `STATICFILES_DIRS`，避免冲突！
# STATICFILES_DIRS = [BASE_DIR / "static"]

# 让 Whitenoise 正确提供静态文件
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-y6zt60wf(_2z#t9ds^sjwd8_1i#k_87qy8^2fk3x#t#mq4lf6x"
FERNET_KEY='ldRd192XUJ0V6gCaLCtlllD98nw313TM_vGtmNCz_OI='
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["urspace.onrender.com", "127.0.0.1", "localhost"]

CSRF_TRUSTED_ORIGINS = ["https://urspace.onrender.com"]



SIMPLEUI_INDEX = 'Urspace Manager'  # 直接修改后台首页标题


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'customers.utils.CustomerTokenAuthentication',
        'employees.utils.OperatorTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',   # 可选，支持会话认证
        'rest_framework.authentication.BasicAuthentication',      # 可选，支持基本认证
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 需要身份验证
    ),
}

# Application definition

INSTALLED_APPS = [
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "customers",
    "employees",
    "rentals",
    "rest_framework"

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "UrSpace.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "UrSpace.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
