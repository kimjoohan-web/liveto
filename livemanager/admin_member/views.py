from datetime import timezone

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from livemanager.admin_member.models import AdminMember
from django.core.paginator import Paginator


# Create your views here.
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
        admin_pw = request.POST.get('admin_pw')
        admin_name = request.POST.get('admin_name')
        admin_email = request.POST.get('admin_email')
        admin_phone = request.POST.get('admin_phone')
        admin_is_superuser = request.POST.get('admin_is_superuser') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.

        # 새로운 AdminMember 객체를 생성하고 저장합니다.
        new_admin = AdminMember(
            admin_id=admin_id,
            admin_pw=admin_pw,
            admin_name=admin_name,
            admin_email=admin_email,
            admin_phone=admin_phone,
            admin_is_superuser=admin_is_superuser
        )
        new_admin.save()

        return redirect(reverse('admin_member:admin_list'))  # 관리자 목록 페이지로 리디렉션합니다.

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

        admin.admin_id = request.POST.get('admin_id')
        if request.POST.get('admin_pw'):
            admin.admin_pw = request.POST.get('admin_pw')  # 비밀번호가 입력된 경우에만 업데이트합니다.
            admin.admin_name = request.POST.get('admin_name')
            admin.admin_email = request.POST.get('admin_email')
            admin.admin_phone = request.POST.get('admin_phone')
            admin.update_at = timezone.now()  # 현재 시간을 업데이트 시간으로 설정합니다.
            admin.admin_is_superuser = request.POST.get('admin_is_superuser') == 'on'  # 체크박스 값에 따라 True/False로 설정합니다.
            admin.save()  # 변경 사항을 저장합니다.
        return redirect(reverse('admin_member:admin_list') + f'?page={page}&kw={kw}&search_field={search_field}')  # 관리자 목록 페이지로 리디렉션합니다.

    return render(request, 'livemanager/admin_member/admin_update.html', {'admin': admin, 'kw': kw, 'page': page, 'search_field': search_field})