from unittest import case

from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone
from board.models import board
from board.form import boardForm
from django.shortcuts import render

# Create your views here.
def index(request):
    year_list = range(2026, 1998, -1)   # 1999~2026 내림차순
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    year_s = request.GET.get('year', '')  # 연도
    stype= request.GET.get('category', '')  # car_check 필드 값
    category = request.GET.get('category', '')  # car_check 필드 값
    if stype == '':
        stype ="인터넷중계방송"       
    else:
        if stype == "webcasting":
            stype = "인터넷생방송"
        elif stype == "relay":
            stype = "영상중계"
        elif stype == "video":
            stype = "영상물제작"
        elif stype == "elearning":
            stype = "e러닝제작"
        
      
    # 현재 년도 불러오기 
    
    if stype == "인터넷중계방송":
        selected_title="인터넷중계방송"
        if year_s=='':  # 연도가 선택되지 않은 경우
            selected_year = int(year_list[0])  # 가장 최근 연도로 설정
        else:
            selected_year = int(year_s)

    else:
        selected_year = None
        selected_title=stype



    # search_field = request.GET.get('search_field', '')  # 검색 필드 (예: 'car_name', 'car_order', 'car_field', 'car_year', 'car_day')



    sql_str="SELECT car_idx," 
    sql_str+="car_name," 
    sql_str+="car_order,"
    sql_str+="car_field," 
    sql_str+="car_year," 
    sql_str+="car_day," 
    sql_str+="car_date," 
    sql_str+="car_url," 
    sql_str+="car_size_h," 
    sql_str+="car_size_w," 
    sql_str+="car_check," 
    sql_str+="car_readnum," 
    sql_str+="car_content "             
    sql_str+=" FROM board WHERE 1 =1 "
    sql_str+=" AND car_field = %s"  
    if selected_year:
        sql_str+=" AND car_year = %s"  # 선택된 연도 필터링    
    if  kw:
        sql_str+=" AND  car_name LIKE %s or car_order LIKE %s or car_day LIKE %s" 

    sql_str+=" ORDER BY car_date DESC,car_idx DESC"

    with connection.cursor() as cursor:
        if kw:
            if selected_year:
                cursor.execute(sql_str, [stype, selected_year, f'%{kw}%', f'%{kw}%', f'%{kw}%'])
            else:
                cursor.execute(sql_str, [stype, f'%{kw}%', f'%{kw}%', f'%{kw}%'])
            board_lists = cursor.fetchall()
        else:
            if selected_year:
                cursor.execute(sql_str, [stype, selected_year])
            else:
                cursor.execute(sql_str, [stype])    
            board_lists = cursor.fetchall() 

   
    
        
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in board_lists] 
   
     
    paginator = Paginator(data, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    return render(request, 'works/index.html', {'year_list': year_list, 'selected_year': selected_year, 'selected_title': selected_title, 'page_obj': page_obj, 'query': kw, 'category': category})