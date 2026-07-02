from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, admin_id, admin_pw=None, **extra_fields):
        if not admin_id:
            raise ValueError("아이디는 필수입니다.")
        user = self.model(admin_id=admin_id, **extra_fields)
        user.set_password(admin_pw) # 비밀번호 암호화 저장
        user.save(using=self._db)
        return user

    def create_superuser(self, admin_id, admin_pw=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(admin_id, admin_pw=admin_pw, **extra_fields)

# 1. models.Model 대신 AbstractBaseUser를 상속받아야 합니다.
class AdminMember(AbstractBaseUser):
    # 2. primary_key=True는 테이블당 한 번만 사용할 수 있습니다. 복합키가 아니라면 하나만 남겨야 합니다.
    admin_idx = models.AutoField(primary_key=True)  
    admin_id = models.CharField(max_length=100, unique=True, db_column='id') # primary_key=True 제거
    
    # 3. AbstractBaseUser가 password 필드를 내장하므로, 기존 DB 컬럼 매핑을 위해 db_column만 지정합니다.
    password = models.CharField(max_length=100, db_column='pwd') 
    
    admin_name = models.CharField(max_length=100) 
    admin_email = models.EmailField(max_length=100, blank=True, null=True) 
    admin_phone = models.CharField(max_length=20, blank=True, null=True) 
    admin_date_joined = models.DateTimeField(default=timezone.now, blank=True, null=True) 
    
    # 4. last_login 필드도 AbstractBaseUser에 내장되어 있으므로 생략하거나 db_column 매핑이 필요하면 아래처럼 적습니다.
    # last_login = models.DateTimeField(blank=True, null=True, db_column='admin_last_login')
    
    is_active  = models.BooleanField(default=True) 
    is_admin  = models.BooleanField(default=False) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'admin_id' 
    REQUIRED_FIELDS = []         

    class Meta:
        db_table = 'admin_member'
        # managed = False 
        verbose_name = '관리자'
        verbose_name_plural = '관리자'
        ordering = ['-admin_idx']

    def __str__(self):
        return self.admin_name
    
    @property
    def is_staff(self):
        return self.is_admin

    # Django 어드민이나 권한 시스템을 완전히 쓰려면 아래 두 메서드도 추가하는 것이 안전합니다.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin