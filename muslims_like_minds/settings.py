from pathlib import Path
import os
import dj_database_url # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'change-this'
DEBUG = True
ALLOWED_HOSTS = ["https://muslimslikeminds.onrender.com"]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # your app
]

MIDDLEWARE = [  
 'whitenoise.middleware.WhiteNoiseMiddleware',
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'muslims_like_minds.urls'

TEMPLATES = [{
 'BACKEND': 'django.template.backends.django.DjangoTemplates',
 'DIRS': [BASE_DIR / 'core/templates'],
 'APP_DIRS': True,
 'OPTIONS': {'context_processors': [
  'django.template.context_processors.debug',
  'django.template.context_processors.request',
  'django.contrib.auth.context_processors.auth',
  'django.contrib.messages.context_processors.messages',
 ]},

}]
WSGI_APPLICATION = 'muslims_like_minds.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core/static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


USE_TZ = True
TIME_ZONE = 'Africa/Lagos'  # or your preferred timezone