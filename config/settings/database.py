from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# Django database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
