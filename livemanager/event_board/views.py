from ast import keyword
from multiprocessing.dummy import connection
from operator import concat

import django
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from httpx import request
from django.utils import timezone
from board.form import boardForm
from django.contrib import messages 
from board.models import board
from django.core.paginator import Paginator
from django.db.models import Q, CharField, Value
from django.db.models.functions import Concat

# Create your views here.
def event_list(request):
    kw = request.GET.get('kw', '')  # 검색어
    category = request.GET.get('category', '')  # 카테고리 인터넷 중계방송, 인터넷 생방송, 영상중계, 영상물제작, e러닝    
    date_from = request.GET.get('date_from', '')  # 시작 날짜
    date_to = request.GET.get('date_to', '')  # 종료 날짜
    page = request.GET.get('page', 1)  # 페이지 번호
    search_field = request.GET.get('search_field', '')  # 검색 필드 (제목, 내용, 작성자 등)
    board_list = board.objects.all().order_by('-car_idx')  # 모든 게시글 가져오기, 최신순으로 정렬

    if search_field and kw:
        if search_field == 'car_name':
            board_list = board_list.filter(car_name__icontains=kw)  # 제목에 검색어가 포함된 게시글 필터링
        elif search_field == 'car_order':
            board_list = board_list.filter(car_order__icontains=kw)  # 내용에 검색어가 포함된 게시글 필터링


    if kw:
        board_list = board_list.filter(Q(car_name__icontains=kw) | Q(car_order__icontains=kw))  # 제목에 검색어가 포함된 게시글 필터링        


    if category :        
            board_list = board_list.filter(car_field=category)  # 선택한 카테고리로 게시글 필터링

    if date_from and date_to:
            board_list = board_list.filter(car_date__range=[date_from, date_to])  # 선택한 날짜 범위로 게시글 필터링


    paginator = Paginator(board_list, 10)  # 페이지네이션 객체 생성
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    stat_total = board_list.count()  # 전체 게시글 수
    stat_vod = board_list.filter(car_url__isnull=False).count()  # VOD가 있는 게시글 수
    stat_no_vod = board_list.filter(car_url__isnull=True).count()  # VOD가 없는 게시글 수    
    
    
    stat_this_month = board.objects.annotate(combined_date=Concat('car_year', Value('.'), 'car_day', output_field=CharField())).filter(combined_date__contains=str(timezone.now().month)).count()  # 이번 달 게시글 수
    stat_no_attach = board_list.filter(car_image__isnull=True).count()  # 첨부파일이 없는 게시글 수
    context = {'board_list': page_obj, 'category': category, 'kw': kw, 'date_from': date_from, 'date_to': date_to, 'search_field': search_field, 'stat_total': stat_total, 'stat_vod': stat_vod, 'stat_no_vod': stat_no_vod, 'stat_this_month': stat_this_month, 'stat_no_attach': stat_no_attach}
               
    return render(request, 'livemanager/event_board/event_list.html', context)

def event_create(request):
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
        return redirect('event_board:event_list')
    else:
        form = boardForm()
    return render(request, 'livemanager/event_board/event_create.html', {'form': form})

def event_update(request, event_idx):
    board_object = board.objects.get(car_idx=event_idx)

    if request.method == 'POST':
        board_object.car_name = request.POST.get('car_name')
        board_object.car_order = request.POST.get('car_order')
        board_object.car_field = request.POST.get('car_field')
        if not board_object.car_field:
            board_object.car_field = "인터넷중계방송"

        board_object.car_year = request.POST.get('car_year')
        board_object.car_day = request.POST.get('car_day')
        board_object.car_date = timezone.now()
        board_object.car_url = request.POST.get('car_url')
        board_object.car_size_h = 0
        board_object.car_size_w = 0
        board_object.car_check = "NO"
        car_content = request.POST.get('car_content')
        if car_content :
            car_content = car_content.replace('\n', '<br>')
            car_content = car_content.replace(' ', '&nbsp;')
            car_content = car_content.replace('\r', '')
            car_content = car_content.replace('\r\n', '<br>')
            board_object.car_content = car_content

        board_object.car_choo = request.POST.get('car_choo') 
        board_object.car_soonwe = request.POST.get('car_soonwe')
        
        if 'car_image' in request.FILES:
            board_object.car_image = request.FILES['car_image']
        
        board_object.save()
        return redirect('event_board:event_detail', event_idx=board_object.car_idx)
    else:
        
        
        return render(request, 'livemanager/event_board/event_update.html', {'board_object': board_object})
    

def event_detail(request, event_idx):

    # 조회수 증가
    # board.objects.filter(car_idx=event_idx).update(car_readnum=board.objects.get(car_idx=event_idx).car_readnum + 1)
    search_field = request.GET.get('search_field', '')  # 검색 필드 (제목, 행사, 작성자 등)
    kw = request.GET.get('kw', '')  # 검색어
    page = request.GET.get('page', 1)  # 페이지 번호
    category = request.GET.get('category', '')  # 카테고리 인터넷 중계

    board_detail = board.objects.get(car_idx=event_idx)
    context = {'object': board_detail, 'search_field': search_field, 'kw': kw, 'page': page, 'category': category}
    return render(request, 'livemanager/event_board/event_detail.html', context)

def event_delete(request, event_idx):
    board_object = board.objects.get(car_idx=event_idx)
    board_object.delete()
    return redirect('event_board:event_list')
    # return render(request, 'livemanager/event_board/event_delete.html', {'object': board_object})


def event_bulk_delete(request):
   
    event_bulk_delete=request.POST.getlist('selected')  # 선택된 게시글의 ID 리스트를 가져옵니다.
    if event_bulk_delete:
        board.objects.filter(car_idx__in=event_bulk_delete).delete()  # 선택된 게시글들을 삭제합니다.
        messages.success(request, f"{len(event_bulk_delete)}개의 게시글이 삭제되었습니다.")  # 삭제 완료 메시지를 추가합니다.
      
    return redirect('event_board:event_list')
