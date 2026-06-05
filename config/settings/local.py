# config/setting/local.py

from ..settings import *
from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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