from urllib import response

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from django.http import Http404
from django.http import JsonResponse
from django.conf import settings
from django.db import connection
#mssql 연결문자



# mssql_str = f"DRIVER={settings.DATABASES['mssql_db']['OPTIONS']['driver']};SERVER={settings.DATABASES['mssql_db']['HOST']};DATABASE={settings.DATABASES['mssql_db']['NAME']};UID={settings.DATABASES['mssql_db']['USER']};PWD={settings.DATABASES['mssql_db']['PASSWORD']};Encrypt={settings.DATABASES['mssql_db']['OPTIONS']['encrypt']};"
       
    
# Create your views here.
def index(request):
    # mssql 연결
    page = request.GET.get('page', '1')  # 페이지   # 페이지 번호, 기본값은 1
    kw = request.GET.get('kw', '')  # 검색어, 기본값은 빈 문자열
    
    # page_obj = None
      
    # mssql_conn = pyodbc.connect(mssql_str)
    # cursor = mssql_conn.cursor()
    # # SQL 쿼리 실행
    # sql_str = "SELECT top 100 * FROM Event_Member order by mem_idx desc"  # 실제 테이블 이름으로 변경
    # cursor.execute(sql_str)  # 실제 테이블 이름으로 변경
    # rows = cursor.fetchall()

    
    
    # # 결과를 리스트로 변환
    # # data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    # paginator_1 = Paginator(rows,int(10))  # 페이지당 10개씩 보여주기  
    # page_obj = paginator_1.get_page(page)  
    # context ={'members':page_obj,'page':page,'kw':kw}
    
    sql_str = "SELECT top 100 * FROM Event_Member order by mem_idx desc"  # 실제 테이블 이름으로 변경
    with connection.cursor() as cursor:
        cursor.execute(sql_str)  # 실제 테이블 이름으로 변경
        rows = cursor.fetchall()

    paginator_1 = Paginator(rows,int(10))  # 페이지당 10개씩 보여주기  
    page_obj = paginator_1.get_page(page)

    context ={'members':page_obj,'page':page,'kw':kw}
    return render(request, 'livemanager/member/member_list.html', context)


def member_input(request):
    if request.method == 'POST':
        # 폼에서 입력된 데이터 처리
        mem_Event = '0'
        mem_name = request.POST.get('mem_name')
        mem_HP = request.POST.get('mem_HP')
        mem_email_arr = []
        mem_email = request.POST.get('mem_email')
        if mem_email: # @가 포함된 이메일이 입력된 경우에만 분리
            if '@' in mem_email:
                mem_email_arr = mem_email.split('@')  # 이메일 @ 기준으로 분리
                mem_email1 = mem_email_arr[0]  # @ 앞 부분
                mem_email2 = mem_email_arr[1]  # @ 뒤 부분

        mem_hospital = request.POST.get('mem_hospital')
        mem_dept = request.POST.get('mem_dept')
        Country = request.POST.get('Country')

        sql_str = f"INSERT INTO Event_Member ("
        sql_str += f" mem_id"
        sql_str += f" ,mem_name"
        sql_str += f", mem_HP "
        sql_str += f", mem_email1"
        sql_str += f", mem_email2"
        sql_str += f", mem_hospital"
        sql_str += f", mem_dept"
        sql_str += f", mem_Event"
        sql_str += f", mem_input_date"
        sql_str += f", Country) VALUES "
        sql_str += f"('{mem_HP}'"
        sql_str += f", '{mem_name}'"
        sql_str += f", '{mem_HP}'"
        sql_str += f", '{mem_email1}'"
        sql_str += f", '{mem_email2}'"
        sql_str += f", '{mem_hospital}'"
        sql_str += f", '{mem_dept}'"
        sql_str += f", '{mem_Event}'"
        sql_str += f", NOW()"
        sql_str += f", '{Country}')"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            connection.commit()

        # 예: name = request.POST.get('name')
        #     email = request.POST.get('email')
        #     ... (다른 필드들도 처리)
        
        # 데이터베이스에 저장하거나 필요한 작업 수행
        # 예: Member.objects.create(name=name, email=email, ...)
        
        # 처리 후 리다이렉트 또는 성공 메시지 반환
        return render(request, 'livemanager/member/member_list.html')
    else:    
        return render(request, 'livemanager/member/member_input.html')
    
def mem_login(request):
    return render(request, 'livemanager/member/login.html') 