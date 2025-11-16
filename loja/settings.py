from pathlib import Path
import os

# Caminho base do projeto
BASE_DIR = Path(_file_).resolve().parent.parent

# SECRET_KEY: pega do ambiente no Render, ou usa uma chave de dev se não existir
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'chave-super-secreta-para-dev')

# Em produção (Render) deixe False. Se quiser debugar local, pode mudar para True.
DEBUG = False

# Domínios autorizados
ALLOWED_HOSTS = [
    'yamaru-store.onrender.com',   # endereço do Render
    'yamarustore.com.br',          # seu domínio (exemplo)
    'www.yamarustore.com.br',      # versão com www
    '127.0.0.1',
    'localhost',
]

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'loja_app',  # seu app da loja
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loja.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # se você tiver pastas extras de template, pode adicionar aqui
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

WSGI_APPLICATION = 'loja.wsgi.application'

# Banco de dados (SQLite – igual ao padrão do Django)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validação de senha
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

# Localização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Manaus'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (CSS, JS, imagens de layout)
STATIC_URL = 'static/'

# Pasta onde o Django vai *coletar* todos os estáticos para produção
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Pasta onde ficam seus arquivos estáticos do projeto (se você tiver /static/)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Arquivos enviados pelo usuário (imagens de produtos, etc.)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'