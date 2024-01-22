from pathlib import Path
from environs import Env
from datetime import timedelta

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")
OPENAI_KEY = env.str("OPENAI_KEY")
SPRINGER_KEY = env.str("SPRINGER_KEY")
DB_PASSWORD = env.str("DB_PASSWORD")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
# DEBUG = False

MAIN_ORIGIN = "https://chatg6.ai"


CURRENT_ORIGIN = "http://localhost:3000" if DEBUG else MAIN_ORIGIN

ALLOWED_HOSTS = [
    "localhost",
    "51.20.38.135",
    ".railway.app",
    ".chatg6.ai",
    "127.0.0.1",
    ".surge.sh",
]


# simple-trip.surge.sh
# longing-believe.surge.sh
# CORS_ALLOWED_ORIGINS = (
#     # "http://localhost:3000",
#     # "http://127.0.0.1:8000",
#     "http://127.0.0.1:3000",
#     # "http://localhost:8000",
#     # "http://51.20.38.135",
#     "https://g6tool.vercel.app",
# )
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# frontendhost
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    # "http://localhost:8000",
    "https://g6tool.vercel.app",
    # "http://simple-trip.surge.sh",
    "https://www.chatg6.ai",
    "https://core.chatg6.ai",
    "https://chatg6.ai",
]  # new


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # third party
    "allauth",
    "allauth.account",
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # local
    "accounts",
    "AI_writing_tools",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "django_main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]


ASGI_APPLICATION = "django_main.asgi.application"
WSGI_APPLICATION = "django_main.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if DEBUG:
    # if False:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            # "ENGINE": "django.db.backends.postgresql",
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD":DB_PASSWORD ,
            "HOST": "database-text.cjvhkxjccfnp.eu-north-1.rds.amazonaws.com",
            "PORT": "5432",
        }
    }
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql_psycopg2",
    #         "NAME": "g6tool",
    #         "USER": "ubuntu",
    #         "PASSWORD": "bbeellaall",
    #         "HOST": "localhost",
    #         "PORT": "",
    #     }
    # }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# for allauth settings


SITE_ID = 1

OLD_PASSWORD_FIELD_ENABLED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True  # new
ACCOUNT_UNIQUE_EMAIL = True  # new
ACCOUNT_EMAIL_VERIFICATION = "optional"  # 'mandatory'
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =3  in days
# ACCOUNT_USERNAME_BLACKLIST =[]
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "app-auth",
    "JWT_AUTH_REFRESH_COOKIE": "refresh-token",
    "REGISTER_SERIALIZER": "accounts.serializers.MyRegisterSerializer",
    "USER_DETAILS_SERIALIZER": "AI_writing_tools.serializers.MyUserDetailsSerializer",
    "JWT_AUTH_HTTPONLY": True,
    "JWT_AUTH_SAMESITE": "None",
    "JWT_AUTH_SECURE": True,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=200),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}


AUTH_USER_MODEL = "accounts.CustomUserModel"

#############################
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
#############################

STATIC_URL = "/static/"
# STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env.str("DEFAULT_FROM_EMAIL")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env.str("GOOGLE_CLIENT_ID"),
            "secret": env.str("GOOGLE_SECRET_KEY"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
        "OAUTH_PKCE_ENABLED": True,
    }
}
