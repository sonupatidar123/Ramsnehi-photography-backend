import os
from pathlib import Path
from datetime import timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api
# 1. Import dj_database_url for easy hosting connection
import dj_database_url 
PORT = os.environ.get("PORT", 10000)
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY SETTINGS ---
# 2. Secret key ko environment variable se uthayein
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-your-fallback-key')

# 3. DEBUG False karein (Production mein False hona MUST hai)
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# 4. Domains allow karein
# ALLOWED_HOSTS = [
#     'localhost',          # Sirf hostname
#     '127.0.0.1',         # Local IP
#     '.vercel.app',       # Subdomains allowed
#     '.onrender.com',     
#     'yourdomain.com'
# ]
ALLOWED_HOSTS = ['ramsnehi-photography-backend.onrender.com']
# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'gallery',
    'cloudinary',
    'cloudinary_storage',
    'whitenoise.runserver_nostatic', # Static files management
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS Top par
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static files optimize karne ke liye
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = DEBUG # Sirf Debug mode mein sab allow karein
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "https://ramsnehi-photography.vercel.app",
    ]
    CSRF_TRUSTED_ORIGINS = ["https://ramsnehi-photography.vercel.app"]
CORS_ALLOW_CREDENTIALS = True

# --- DATABASE (Supabase Optimization) ---
# DATABASES = {
#     'default': dj_database_url.config(
#         default=f"postgresql://postgres.wdydpnqymvigsistlqyk:{os.environ.get('DB_PASSWORD', '@Egsonu9770')}@aws-1-ap-south-1.pooler.supabase.com:6543/postgres",
#         conn_max_age=600,
#         ssl_require=True
#     )
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- CLOUDINARY ---
cloudinary.config( 
    cloud_name = os.environ.get('CLOUDINARY_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'), 
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- SECURITY ENHANCEMENTS (Only for Live) ---
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # ✅ IMPORTANT
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --- STATIC FILES (WhiteNoise) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ---------------------------------------------------------------------------
# Admin & Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ROOT_URLCONF = 'ramsnehi.urls'
WSGI_APPLICATION = 'ramsnehi.wsgi.application'

# Admin Branding
ADMIN_SITE_HEADER = 'Ramsnehi Photography Admin'
ADMIN_SITE_TITLE  = 'Ramsnehi Photography'
ADMIN_INDEX_TITLE = 'Content Management Dashboard'

# Thumbnail Settings
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
