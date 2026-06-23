from ast import Not

from django.db import connection
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import board
from .form import boardForm
from django.core.paginator import Paginator



# Create your views here.
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    search_field = request.GET.get('search_field', '')  # 검색 필드 (예: 'car_name', 'car_order', 'car_field', 'car_year', 'car_day')
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
    if search_field and kw:
        sql_str+=" AND " + search_field + " LIKE %s ORDER BY car_date DESC,car_idx DESC" 

    with connection.cursor() as cursor:
        if search_field and kw:
            cursor.execute(sql_str, [f'%{kw}%'])
            board_lists = cursor.fetchall()
        else:
            cursor.execute(sql_str)
            board_lists = cursor.fetchall()
    
        
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in board_lists] 
   
     
    paginator = Paginator(data, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'board_list': page_obj, 'page': page, 'kw': kw, 'search_field': search_field }
       

    return render(request, 'board/index.html', context)

def board_create(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        car_order = request.POST.get('car_order')
        car_field = request.POST.get('car_field')
        if not car_field:
            car_field = "인터넷중계방송"

        car_year = request.POST.get('car_year')
        car_day = request.POST.get('car_day')
        car_date = timezone.now()
        car_url = request.POST.get('car_url')
        car_size_h = 0
        car_size_w = 0
        car_check = "NO"
        car_content = request.POST.get('car_content')
        if car_content :
            car_content = car_content.replace('\n', '<br>')
            car_content = car_content.replace(' ', '&nbsp;')
            car_content = car_content.replace('\r', '')
            car_content = car_content.replace('\r\n', '<br>')

            

        
        car_choo = request.POST.get('car_choo') 
        car_soonwe = request.POST.get('car_soonwe')
        car_readnum = 0 
        car_image = request.FILES.get('car_image')
        # 저장 장소
       
        

        board.objects.create(
            car_name=car_name,
            car_order=car_order,
            car_field=car_field,
            car_year=car_year,
            car_day=car_day,
            car_date=car_date,
            car_url=car_url,
            car_size_h=car_size_h,
            car_size_w=car_size_w,
            car_check=car_check,
            car_content=car_content,
            car_image=car_image,
            car_choo=car_choo,
            car_soonwe=car_soonwe,
            car_readnum=car_readnum,
            
        )
        return redirect('board:index')
    else:
        form = boardForm()
    return render(request, 'board/board_input.html', {'form': form})

def board_detail(request, car_idx):
    # 조회수 증가
    board.objects.filter(car_idx=car_idx).update(car_readnum=board.objects.get(car_idx=car_idx).car_readnum + 1)

    board_detail = board.objects.get(car_idx=car_idx)
    context = {'board_detail': board_detail}
    return render(request, 'board/board_detail.html', context)

def board_update(request, car_idx):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        car_order = request.POST.get('car_order')
        car_field = request.POST.get('car_field')
        if not car_field:
            car_field = "인터넷중계방송"

        car_year = request.POST.get('car_year')
        car_day = request.POST.get('car_day')
        car_date = timezone.now()
        car_url = request.POST.get('car_url')
        car_size_h = 0
        car_size_w = 0
        car_check = "NO"
        car_content = request.POST.get('car_content')
        if car_content :
            car_content = car_content.replace('\n', '<br>')
            car_content = car_content.replace(' ', '&nbsp;')
            car_content = car_content.replace('\r', '')
            car_content = car_content.replace('\r\n', '<br>')




        car_choo = request.POST.get('car_choo') 
        car_soonwe = request.POST.get('car_soonwe')        
        car_image = request.FILES.get('car_image')
        delete_images = request.POST.get('delete_images')  # 삭제할 이미지의 ID 리스트
        if not car_image and delete_images:
            car_image = None  # 이미지만 삭제 시 None으로 설정

       

        sql_up="UPDATE board SET car_name=%s, " \
                                "car_order=%s" \
                                ", car_field=%s" \
                                ", car_year=%s" \
                                ", car_day=%s" \
                                ", car_date=%s" \
                                ", car_url=%s" \
                                ", car_size_h=%s" \
                                ", car_size_w=%s" \
                                ", car_check=%s" \
                                ", car_content=%s" \
                                ", car_choo=%s" \
                                ", car_soonwe=%s WHERE car_idx = %s"
    
        with connection.cursor() as cursor:
            cursor.execute(sql_up, 
                           [car_name
                            , car_order
                            , car_field
                            , car_year
                            , car_day
                            , car_date
                            , car_url
                            , car_size_h
                            , car_size_w
                            , car_check
                            , car_content                            
                            , car_choo
                            , car_soonwe
                            , car_idx]
                           )
        #업로드 파일 
        board_upload = board.objects.get(car_idx=car_idx)
        if car_image:
            board_upload.car_image = car_image
            board.objects.filter(car_idx=car_idx).update(car_image=car_image)
            board_upload.save() 
        else:
                board_upload.car_image = None
                board.objects.filter(car_idx=car_idx).update(car_image=None)
                board_upload.save()   
                

       
        return redirect('board:board_detail', car_idx=car_idx)
    else:
        board_update = board.objects.get(car_idx=car_idx)
        form = boardForm(instance=board_update)
        
    return render(request, 'board/board_update.html', {'form': form, 'car_idx': car_idx})
    


def board_delete(request, car_idx):
    board_delete = board.objects.get(car_idx=car_idx)
    board_delete.delete()
    return redirect('board:index')