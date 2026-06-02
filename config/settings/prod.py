
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

STATIC_URL = 'static/'
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
    },
    'mssql_db': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'nicejoodding',       # MSSQL DB 이름
        'USER': 'nicejoodding',             # 예: sa
        'PASSWORD': 'fdkwon8824@',            # DB 접속 패스워드
        'HOST': 'wws12-002.cafe24.com',    # 로컬인 경우 'localhost' 또는 '127.0.0.1'
        'PORT': '1433',                  # MSSQL 기본 포트
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server', # 설치된 ODBC 버전에 맞게 수정 (예: 18 등)            
            'encrypt': 'no',  # SSL 암호화 비활성화 (개발 환경에서만 사용)
        },
    },
}