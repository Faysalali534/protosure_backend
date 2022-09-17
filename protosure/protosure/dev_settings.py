from protosure.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME", default="protosure"),
        'USER': env("DATABASE_USER", default="postgres"),
        'PASSWORD': env("DATABASE_PASSWORD", default="postgres"),
        'HOST': env("DATABASE_HOST", default="localhost"),
        'PORT': env.int("DATABASE_PORT", default=5432)
    }
}