import os
from pathlib import Path
from datetime import timedelta
import urllib.parse
import cloudinary
import cloudinary.uploader
import cloudinary.api
# 1. Import dj_database_url for easy hosting connection
import dj_database_url 
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", 'django-insecure-please-change-me')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# 4. Domains allow karein
ALLOWED_HOSTS = [
    'ramsnehi-photography-backend.onrender.com',
    'ramsnehi-photography.vercel.app',
    '127.0.0.1',
    'localhost', 

]
# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',          # ✅ JWT
    'rest_framework_simplejwt.token_blacklist',  # ✅ enables token invalidation on logout
    'corsheaders',
    'django_filters',
    'gallery',
    'cloudinary',
    'cloudinary_storage',
    'whitenoise.runserver_nostatic',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'corsheaders.middleware.CorsMiddleware',       # ✅ must be at top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- ✅ REST FRAMEWORK (THIS WAS MISSING — ROOT CAUSE OF 401 ERRORS) ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# --- ✅ JWT SETTINGS ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,    # ✅ gives a new refresh token on every refresh call
    'BLACKLIST_AFTER_ROTATION': True,  # ✅ old refresh token becomes invalid after rotation
    'AUTH_HEADER_TYPES': ('Bearer',),
    'UPDATE_LAST_LOGIN': True,
}

# --- CORS ---
# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
]

if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
       

        "https://ramsnehi-photography.vercel.app",
        "https://ramsnehi-photography-frontend.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    CSRF_TRUSTED_ORIGINS = [

        "https://ramsnehi-photography.vercel.app",
        "https://ramsnehi-photography-frontend.vercel.app",

        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",

    ]
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]
CORS_ALLOW_CREDENTIALS = True
# Redis (use Render's Redis or Upstash — free tier available)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 60 * 15,  # 15 minutes default
        'IGNORE_EXCEPTIONS': True,
    }
}

# Use cache for Django sessions too (bonus)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
# --- DATABASE (Supabase Optimization) ---

db_password = os.environ.get('DB_PASSWORD')
encoded_password = urllib.parse.quote_plus(db_password)

DATABASES = {
    'default': dj_database_url.config(
        default=f"postgresql://postgres.wdydpnqymvigsistlqyk:{encoded_password}@aws-1-ap-south-1.pooler.supabase.com:6543/postgres",
        
        conn_max_age=300,
        ssl_require=True
    )
}

# --

# --- CLOUDINARY ---
cloudinary.config( 
    cloud_name = os.environ.get('CLOUDINARY_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'), 
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- SECURITY (Production only) ---
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --- STATIC FILES ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- INTERNATIONALISATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ROOT_URLCONF = 'ramsnehi.urls'
WSGI_APPLICATION = 'ramsnehi.wsgi.application'

# --- ADMIN BRANDING ---
ADMIN_SITE_HEADER = 'Ramsnehi Photography Admin'
ADMIN_SITE_TITLE  = 'Ramsnehi Photography'
ADMIN_INDEX_TITLE = 'Content Management Dashboard'

THUMBNAIL_QUALITY = 95
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PRESERVE_FORMAT = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
