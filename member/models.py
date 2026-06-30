from django.db import models

class event_member(models.Model):
    mem_idx = models.AutoField(primary_key=True)  # 자동 증가
    mem_id = models.CharField(max_length=50)  # 회원 아이디를 나타내는 필드입니다.
    mem_name = models.CharField(max_length=200, blank=True, null=True)  # 회원 이름을 나타내는 필드입니다.
    mem_hospital = models.CharField(max_length=500, blank=True, null=True)  # 회원 병원을 나타내는 필드입니다.
    mem_email1 = models.CharField(max_length=100, blank=True, null=True)  # 회원 이메일을 나타내는 필드입니다.
    mem_email2 = models.CharField(max_length=100, blank=True, null=True)  # 회원 이메일을 나타내는 필드입니다.
    mem_HP = models.CharField(max_length=50, blank=True, null=True)  # 회원 휴대폰 번호를 나타내는 필드입니다.
    mem_Event = models.SmallIntegerField()  # 회원 이벤트를 나타내는 필드입니다.
    zipcode = models.CharField(max_length=6, blank=True, null=True)  # 우편번호를 나타내는 필드입니다.
    mem_address1 = models.CharField(max_length=100, blank=True, null=True)  # 회원 주소를 나타내는 필드입니다.
    mem_address2 = models.CharField(max_length=100, blank=True, null=True)  # 회원 상세 주소를 나타내는 필드입니다.
    mem_hos_tel = models.CharField(max_length=20, blank=True, null=True)  # 회원 병원 전화번호를 나타내는 필드입니다.
    mem_input_date = models.DateTimeField()  # 회원 입력 날짜를 나타내는 필드입니다.
    Event_location = models.CharField(max_length=1, blank=True, null=True)  # 이벤트 위치를 나타내는 필드입니다.
    mem_Depart = models.CharField(max_length=100, blank=True, null=True)  # 회원 부서를 나타내는 필드입니다.
    mem_teamName = models.CharField(max_length=200, blank=True, null=True)  # 회원 팀 이름을 나타내는 필드입니다.
    mem_SalesName = models.CharField(max_length=200, blank=True, null=True)  # 회원 영업 이름을 나타내는 필드입니다.
    mem_duty = models.CharField(max_length=100, blank=True, null=True)  # 회원 직무를 나타내는 필드입니다.
    mem_YN = models.CharField(max_length=1, blank=True, null=True)  # 회원 여부를 나타내는 필드입니다.
    Country = models.CharField(max_length=200, blank=True, null=True)  # 회원 국가를 나타내는 필드입니다.
    LastName = models.CharField(max_length=100, blank=True, null=True)  # 회원 성을 나타내는 필드입니다.
    mem_dept = models.CharField(max_length=500, blank=True, null=True)  # 회원 부서를 나타내는 필드입니다.
    account_code = models.CharField(max_length=30, blank=True, null=True)  # 회원 계정 코드를 나타내는 필드입니다.
    use_YN = models.CharField(max_length=1, blank=True, null=True)  # 사용 여부를 나타내는 필드입니다.
    mem_pwd = models.CharField(max_length=20, blank=True, null=True)  # 회원 비밀번호를 나타내는 필드입니다.
    dc_licence = models.CharField(max_length=30, blank=True, null=True)  # 회원 면허를 나타내는 필드입니다.
    connect_path = models.CharField(max_length=1, blank=True, null=True)  # 연결 경로를 나타내는 필드입니다.
    etc_text = models.CharField(max_length=500, blank=True, null=True)  # 기타 정보를 나타내는 필드입니다.
    event_gubun = models.CharField(max_length=1, blank=True, null=True)  # 이벤트 구분을 나타내는 필드입니다.
    work_id = models.CharField(max_length=50, blank=True, null=True)  # 작업 ID를 나타내는 필드입니다.
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)  # 가격을 나타내는 필드입니다.
    depositor = models.CharField(max_length=100, blank=True, null=True)  # 예금주를 나타내는 필드입니다.
    due_date = models.CharField(max_length=8, blank=True, null=True)  # 만기일을 나타내는 필드입니다.
    mail_YN = models.CharField(max_length=1, blank=True, null=True)  # 메일 여부를 나타내는 필드입니다.
    memTranspor = models.CharField(max_length=1, blank=True, null=True)  # 회원 운송 여부를 나타내는 필드입니다.
    mem_birth = models.CharField(max_length=8, blank=True, null=True)  # 회원 생년월일을 나타내는 필드입니다.
    mem_sex = models.CharField(max_length=1, blank=True, null=True)  # 회원 성별을 나타내는 필드입니다.
    FirstName = models.CharField(max_length=200, blank=True, null=True)  # 회원 이름을 나타내는 필드입니다.
    mem_agree = models.CharField(max_length=1, blank=True, null=True)  # 회원 동의 여부를 나타내는 필드입니다.
    hospital_address = models.CharField(max_length=200, blank=True, null=True)  # 병원 주소를 나타내는 필드입니다.
    Affiliation = models.CharField(max_length=100, blank=True, null=True)  # 소속을 나타내는 필드입니다.
    Dietary = models.CharField(max_length=30, blank=True, null=True)  # 식이 정보를 나타내는 필드입니다.
    Dietary_Etc = models.CharField(max_length=500, blank=True, null=True)  # 기타 식이 정보를 나타내는 필드입니다.
    mem_Depart_kor = models.CharField(max_length=200, blank=True, null=True)  # 회원 부서를 나타내는 필드입니다.
    mem_Text = models.CharField(max_length=2000, blank=True, null=True)  # 회원 텍스트 정보를 나타내는 필드입니다.
    mem_name_eng = models.CharField(max_length=200, blank=True, null=True)  # 회원 이름(영문)을 나타내는 필드입니다.
    mem_hospital_eng = models.CharField(max_length=500, blank=True, null=True)  # 병원 이름(영문)을 나타내는 필드입니다.
    tp1 = models.CharField(max_length=30, blank=True, null=True)  # 추가 정보를 나타내는 필드입니다.
    tp2 = models.CharField(max_length=30, blank=True, null=True)  # 추가 정보를 나타내는 필드입니다.
    tp3 = models.CharField(max_length=30, blank=True, null=True)  # 추가 정보를 나타내는 필드입니다.
    tp4 = models.CharField(max_length=30, blank=True, null=True)  # 추가 정보를 나타내는 필드입니다.
    Allergy = models.CharField(max_length=30, blank=True, null=True)  # 알레르기 정보를 나타내는 필드입니다.
    Allergy_Etc = models.CharField(max_length=500, blank=True, null=True)  # 기타 알레르기 정보를 나타내는 필드입니다.
    DelType = models.CharField(max_length=1, default='N', blank=True, null=True)  # 삭제 유형을 나타내는 필드입니다.
    DelDate = models.DateTimeField(blank=True, null=True)  # 삭제 날짜를 나타내는 필드입니다.
    add_info = models.CharField(max_length=50, blank=True, null=True)  # 추가 정보를 나타내는 필드입니다.


    class Meta:
        db_table = 'event_member'
        verbose_name = '회원'
        verbose_name_plural = '회원'
        ordering = ['-mem_idx']

    def __str__(self):
        return self.mem_name
