from django.db import models
from django.utils import timezone
# Create your models here.

class AdminMember(models.Model):
    admin_idx = models.AutoField(primary_key=True)  # 자동 증가
    admin_id = models.CharField(max_length=100) # 관리자 아이디를 나타내는 필드입니다.
    admin_pw = models.CharField(max_length=100) # 관리자 비밀번호를 나타내는 필드입니다.
    admin_name = models.CharField(max_length=100) # 관리자 이름을 나타내는 필드입니다.
    admin_email = models.EmailField(max_length=100, blank=True, null=True) # 관리자 이메일을 나타내는 필드입니다. 이메일 주소를 저장하며, 빈 값이나 null 값을 허용합니다.
    admin_phone = models.CharField(max_length=20, blank=True, null=True) # 관리자 전화번호를 나타내는 필드입니다.
    admin_date_joined = models.DateTimeField(default=timezone.now, blank=True, null=True) # 계정 생성 시간을 나타내는 필드입니다. 사용자가 계정을 생성한 시간을 기록합니다.
    admin_last_login = models.DateTimeField(blank=True, null=True) # 마지막 로그인 시간을 나타내는 필드입니다. 사용자가 마지막으로 로그인한 시간을 기록합니다.
    admin_is_active = models.BooleanField(default=True) # 관리자 계정 활성화 여부를 나타내는 필드입니다. True이면 활성화된 계정, False이면 비활성화된 계정을 의미합니다.
    admin_is_superuser = models.BooleanField(default=False) # 관리자 등급을 만들수 있는 메뉴가 필요하다면 이 필드를 활용할 수 있습니다.

    class Meta:
        db_table = 'admin_member'
        verbose_name = '관리자'
        verbose_name_plural = '관리자'
        ordering = ['-admin_idx']

    def __str__(self):
        return self.admin_name
