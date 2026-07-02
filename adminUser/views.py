from os import path

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils import timezone
from httpx import request
from adminUser.models import AdminMember
from board import admin, views
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 폼 검증이 성공하면 유저 객체를 반환받음
            user = form.get_user()
            login(request, user) # 세션에 로그인 정보 기록
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('adminUser:admin_dashboard') # 본인의 기본 메인 뷰 이름으로 변경

    else:
        form = AuthenticationForm()
        
    return render(request, 'livemanager/admin_login.html', {'form': form})



def admin_login(request):
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        admin_pw = request.POST.get('admin_password')

        # 사용자 인증
        user = authenticate(request, username=admin_id, password=admin_pw)

        if user is not None:
            # 로그인 성공
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('livemanager:admin_dashboard') # 본인의 기본 메인 뷰 이름으로 변경
        else:
            # 로그인 실패
            error_message = "아이디 또는 비밀번호가 올바르지 않습니다."
            return render(request, 'livemanager/admin_login.html', {'error_message': error_message})
    
    return render(request, 'livemanager/admin_login.html')


def admin_logout(request):
    # 로그아웃 처리
    from django.contrib.auth import logout
    logout(request)
    return redirect('adminUser:admin_login')  # 로그아웃 후 리다이렉트할 URL 이름


def admin_dashboard(request):
    # 관리자 대시보드 페이지 렌더링
    if not request.user.is_authenticated:
        return redirect('adminUser:admin_login')  # 로그인 페이지로 리다이렉트   

    return render(request, 'livemanager/admin_dashboard.html')


def index(request):
    return render(request, 'livemanager/index.html')    

@login_required(login_url='adminUser:admin_login')  # 로그인하지 않은 경우 admin_login 페이지로 리다이렉트
def admin_list(request):
    page = request.GET.get('page', 1)  # 페이지 번호를 가져옵니다. 기본값은 1입니다.
    search_field = request.GET.get('search_field', '')  # 검색 필드를 가져옵니다. search_field라는 이름으로 GET 요청에서 검색 필드를 가져옵니다.
    kw = request.GET.get('kw', '')  # 검색어를 가져옵니다. kw라는 이름으로 GET 요청에서 검색어를 가져옵니다.
    admin_lists = AdminMember.objects.all()  # AdminMember 모델의 모든 객체를 가져옵니다.
    
    if kw:
        if search_field == 'name':
            admin_lists = admin_lists.filter(admin_name__icontains=kw)  # 검색어가 있는 경우, 관리자 이름에 검색어가 포함된 객체들로 필터링합니다.
        elif search_field == 'login_id':
            admin_lists = admin_lists.filter(admin_id__icontains=kw)  # 검색어가 있는 경우, 관리자 아이디에 검색어가 포함된 객체들로 필터링합니다.
        elif search_field == 'email':
            admin_lists = admin_lists.filter(admin_email__icontains=kw)  # 검색어가 있는 경우, 관리자 이메일에 검색어가 포함된 객체들로 필터링합니다.


    Pagination = 10  # 한 페이지에 표시할 항목 수
    paginator = Paginator(admin_lists, Pagination)  # Paginator 객체를 생성합니다.
    admin_lists = paginator.get_page(page)  # 요청된 페이지 번호에 해당하는 객체들을 가져옵니다.

    return render(request, 'livemanager/admin_member/admin_list.html', {'admin_lists': admin_lists, 'page': page, 'kw': kw, 'search_field': search_field})


def admin_create(request):

    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        admin_pw = request.POST.get('admin_pw') #패스워드를 암호화하여 저장하는 로직을 추가해야 합니다.
        if admin_pw:
            admin_pw = make_password(admin_pw)  # 비밀번호를 암호화합니다.
        
        admin_name = request.POST.get('admin_name')
        admin_email = request.POST.get('admin_email')
        admin_phone = request.POST.get('admin_phone')
        # admin_is_superuser = request.POST.get('admin_is_superuser') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.
        admin_is_active = request.POST.get('admin_is_active') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.
        admin_is_admin = request.POST.get('admin_is_admin') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.
        # 새로운 AdminMember 객체를 생성하고 저장합니다.
        new_admin = AdminMember(
            admin_id=admin_id,
            password=admin_pw,
            admin_name=admin_name,
            admin_email=admin_email,
            admin_phone=admin_phone,
            admin_date_joined=timezone.now()           
            # is_active=admin_is_active,
            # is_admin=admin_is_admin
        )
        new_admin.save()

        return redirect(reverse('adminUser:admin_list'))  # 관리자 목록 페이지로 리디렉션합니다.

    return render(request, 'livemanager/admin_member/admin_create.html')

def admin_detail(request, admin_idx):
    kw = request.GET.get('kw', '')  # 검색어를 가져옵니다. kw라는 이름으로 GET 요청에서 검색어를 가져옵니다.
    page = request.GET.get('page', 1)  # 페이지 번호를 가져옵니다. 기본값은 1입니다.
    search_field = request.GET.get('search_field', '')  # 검색 필드를 가져옵니다. search_field라는 이름으로 GET 요청에서 검색 필드를 가져옵니다.

    admin = AdminMember.objects.get(admin_idx=admin_idx)  # admin_idx에 해당하는 AdminMember 객체를 가져옵니다.
    return render(request, 'livemanager/admin_member/admin_detail.html', {'admin': admin, 'kw': kw, 'page': page, 'search_field': search_field})

def admin_update(request, admin_idx):
    page = request.GET.get('page', 1)  # 페이지 번호를 가져옵니다. 기본값은 1입니다.
    search_field = request.GET.get('search_field', '')  # 검색 필드를 가져옵니다. search_field라는 이름으로 GET 요청에서 검색 필드를 가져옵니다.
    kw = request.GET.get('kw', '')  # 검색어를 가져옵니다. kw라는 이름으로 GET 요청에서 검색어를 가져옵니다.


    admin = AdminMember.objects.get(admin_idx=admin_idx)  # admin_idx에 해당하는 AdminMember 객체를 가져옵니다.
    if request.method == 'POST':

            admin.admin_id= request.POST.get('admin_id')
            if request.POST.get('admin_pw'):    
                admin.password = make_password(request.POST.get('admin_pw'))  # 비밀번호가 입력된 경우에만 업데이트합니다.
                    
            admin.admin_name = request.POST.get('admin_name')
            admin.admin_email = request.POST.get('admin_email')
            admin.admin_phone = request.POST.get('admin_phone')            
            # admin.admin_is_superuser = request.POST.get('admin_is_superuser') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.
            # admin.admin_is_active = request.POST.get('admin_is_active') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.
            # admin.admin_is_admin = request.POST.get('admin_is_admin') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.
            admin.save()  # 변경 사항을 저장합니다.

            return redirect(reverse('adminUser:admin_list') + f'?page={page}&kw={kw}&search_field={search_field}')  # 관리자 목록 페이지로 리디렉션합니다.
    else:

        return render(request, 'livemanager/admin_member/admin_update.html', {'admin': admin, 'kw': kw, 'page': page, 'search_field': search_field})


def admin_delete(request, admin_idx):
    admin = AdminMember.objects.get(admin_idx=admin_idx)
    admin.delete()
    return redirect(reverse('adminUser:admin_list'))

def admin_detail(request, admin_idx):
    kw = request.GET.get('kw', '')  # 검색어를 가져옵니다. kw라는 이름으로 GET 요청에서 검색어를 가져옵니다.
    page = request.GET.get('page', 1)  # 페이지 번호를 가져옵니다. 기본값은 1입니다.
    search_field = request.GET.get('search_field', '')  # 검색 필드를 가져옵니다. search_field라는 이름으로 GET 요청에서 검색 필드를 가져옵니다.

    admin = AdminMember.objects.get(admin_idx=admin_idx)  # admin_idx에 해당하는 AdminMember 객체를 가져옵니다.
    return render(request, 'livemanager/admin_member/admin_detail.html', {'admin': admin, 'kw': kw, 'page': page, 'search_field': search_field})

