import os
from pathlib import Path
from datetime import timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api
# 1. Import dj_database_url for easy hosting connection
import dj_database_url 

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-your-fallback-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# 4. Domains allow karein
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.vercel.app',    # Frontend Vercel ke liye
    '.onrender.com',  # Backend Render ke liye
    'yourdomain.com'  # Agar koi custom domain hai
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
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,    # ✅ gives a new refresh token on every refresh call
    'BLACKLIST_AFTER_ROTATION': True,  # ✅ old refresh token becomes invalid after rotation
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = DEBUG # Sirf Debug mode mein sab allow karein
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "https://ramsnehi-photography.vercel.app",  # ✅ your frontend
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://ramsnehi-photography.vercel.app",
    ]

CORS_ALLOW_CREDENTIALS = True

# --- DATABASE (Supabase Optimization) ---
DATABASES = {
    'default': dj_database_url.config(
        default=f"postgresql://postgres.wdydpnqymvigsistlqyk:{os.environ.get('DB_PASSWORD', '@Egsonu9770')}@aws-1-ap-south-1.pooler.supabase.com:6543/postgres",
        conn_max_age=600,
        ssl_require=True
    )
}

# --

# --- CLOUDINARY ---
cloudinary.config( 
    cloud_name = os.environ.get('CLOUDINARY_NAME', 'dguujmj75'),
    api_key = os.environ.get('CLOUDINARY_API_KEY', '674752937135479'), 
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'HiFvbp-AOwcf_1fbwnRh0zW7KeI'),
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
