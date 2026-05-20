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
import pyodbc


mssql_str = f"DRIVER={settings.DATABASES['mssql_db']['OPTIONS']['driver']};SERVER={settings.DATABASES['mssql_db']['HOST']};DATABASE={settings.DATABASES['mssql_db']['NAME']};UID={settings.DATABASES['mssql_db']['USER']};PWD={settings.DATABASES['mssql_db']['PASSWORD']}"
       
    
# Create your views here.
def index(request):
    # mssql 연결
    page = request.GET.get('page', '1')  # 페이지   # 페이지 번호, 기본값은 1
    kw = request.GET.get('kw', '')  # 검색어, 기본값은 빈 문자열
    
    page_obj = None
      
    mssql_conn = pyodbc.connect(mssql_str)
    cursor = mssql_conn.cursor()
    # SQL 쿼리 실행
    sql_str = "SELECT top 100 * FROM Event_Member order by mem_idx desc"  # 실제 테이블 이름으로 변경
    cursor.execute(sql_str)  # 실제 테이블 이름으로 변경
    rows = cursor.fetchall()

    
    
    # 결과를 리스트로 변환
    # data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    paginator_1 = Paginator(rows,int(10))  # 페이지당 10개씩 보여주기  
    page_obj = paginator_1.get_page(page)  
    context ={'members':page_obj,'page':page,'kw':kw}
    
    return render(request, 'livemanager/member/member_list.html', context)