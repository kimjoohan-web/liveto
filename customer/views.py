from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import connection
from board.models import board


# Create your views here.
def index(request):
    
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어    
    # category = request.GET.get('category', '')  # car_check 필드 값
    stype ='인터넷 중계'

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
           
    if  kw:
        sql_str+=" AND  car_name LIKE %s or car_order LIKE %s or car_day LIKE %s" 

    sql_str+=" ORDER BY car_date DESC,car_idx DESC"

 
    with connection.cursor() as cursor:
        if kw:
            cursor.execute(sql_str, [ f'%{kw}%', f'%{kw}%', f'%{kw}%'])
            board_lists = cursor.fetchall()
        else:
            
            cursor.execute(sql_str)    
            board_lists = cursor.fetchall() 

   
    
        
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in board_lists] 
   
     
    paginator = Paginator(data, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    return render(request, 'customer/customer_board_list.html', {'page_obj': page_obj, 'kw': kw, 'stype': stype})

def detail(request, car_idx):
        
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
        sql_str+=" FROM board WHERE car_idx = %s"
        
        with connection.cursor() as cursor:
            cursor.execute(sql_str, [car_idx])
            board_detail = cursor.fetchone()
            data = dict(zip([column[0] for column in cursor.description], board_detail)) if board_detail else None
        return render(request, 'customer/customer_board_detail.html', {'data': data})


def contact(request):
    return render(request, 'customer/customer_contact.html')

def privacy(request):
    return render(request, 'customer/customer_privacy.html')