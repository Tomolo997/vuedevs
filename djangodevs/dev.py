from .base import * 
import os
#overwrite base settings here 
DEBUG=True
ADMIN_ENABLED = True
STRIPE_LIVE_MODE = True 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dd',
        'USER':  "postgres",
        'PASSWORD':"rootUser",
        'HOST': "localhost",
        'PORT': '5433'
    }
}