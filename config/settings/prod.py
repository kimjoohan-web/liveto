
import environ
from .base import *

# ALLOWED_HOSTS = ['43.201.107.113','127.0.0.1','localhost']
ALLOWED_HOSTS = ['*']

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')





# STATIC_ROOT = BASE_DIR / 'static/'


# STATICFILES_DIRS = []
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#    BASE_DIR / 'static/',  
   
# ]

# STATIC_ROOT = '/static/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '../static/'
STATICFILES_DIRS = [
   BASE_DIR /'static/',  
   
]

# STATIC_ROOT = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR,'/static/')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    }
}