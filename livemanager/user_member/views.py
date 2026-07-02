from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from member.models import event_member
from django.core.paginator import Paginator
from django.utils import timezone  
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='adminUser:admin_login')  # 로그인하지 않은 경우 admin_login 페이지로 리다이렉트
def user_list(request):

    page = request.GET.get('page', 1)  # 페이지 번호를 가져옵니다. 기본값은 1입니다.
    kw = request.GET.get('kw', '')  # 검색어를 가져옵니다. kw라는 이름으로 GET 요청에서 검색어를 가져옵니다.
    search_field = request.GET.get('search_field', '')  # 검색 필드를 가져옵니다. search_field라는 이름으로 GET 요청에서 검색 필드를 가져옵니다.

    members = event_member.objects.all()  # event_member 모델의 모든 객체를 가져옵니다.
    if kw:
        if search_field == 'name':
            members = members.filter(mem_name__icontains=kw)  # 검색어가 있는 경우, 회원 이름에 검색어가 포함된 객체들로 필터링합니다.
        elif search_field == 'id':
            members = members.filter(mem_id__icontains=kw)  # 검색어가 있는 경우, 회원 아이디에 검색어가 포함된 객체들로 필터링합니다.
        elif search_field == 'email':
            members = members.filter(mem_email__icontains=kw)  # 검색어가 있는 경우, 회원 이메일에 검색어가 포함된 객체들로 필터링합니다.
    paginator = Paginator(members, 10)  # 한 페이지에 표시할 항목 수를 10으로 설정합니다.
    page_obj = paginator.get_page(page)   
    

    return render(request, 'livemanager/user_member/member_list.html', {'page_obj': page_obj, 'kw': kw, 'search_field': search_field})
    
@login_required(login_url='adminUser:admin_login')  # 로그인하지 않은 경우 admin_login 페이지로 리다이렉트      
def user_create(request):
    if request.method == 'POST':
        mem_id = request.POST.get('mem_id')
        mem_name = request.POST.get('mem_name')
        mem_HP = request.POST.get('mem_HP')
        mem_email = request.POST.get('mem_email')
        if mem_email:
            if '@' in mem_email:
                arr_email = mem_email.split('@')
                mem_email1=arr_email[0]
                mem_email2=arr_email[1]

        
            
        mem_Event = request.POST.get('mem_Event')
        # 새로운 event_member 객체를 생성하고 저장합니다.
        new_member = event_member(
            mem_id=mem_id,
            mem_name=mem_name,
            mem_HP=mem_HP,
            mem_email1=mem_email1,
            mem_email2=mem_email2,
            mem_Event=mem_Event,
            mem_YN='Y',  # 기본값으로 'Y'를 설정합니다.            
            mem_input_date=timezone.now()  # 현재 시간을 입력 날짜로 설정합니다.
        )
        new_member.save()

        return redirect(reverse('user_member:user_list'))  # 회원 목록 페이지로 리디렉션합니다.
    return render(request, 'livemanager/user_member/member_create.html')
    
@login_required(login_url='adminUser:admin_login')  # 로그인하지 않은 경우 admin_login 페이지로 리다이렉트      
def user_update(request, user_idx,kw='', page=1, search_field=''):
    kw = request.GET.get('kw', '')  # 검색어를 가져옵니다. kw라는 이름으로 GET 요청에서 검색어를 가져옵니다.
    page = request.GET.get('page', 1)  # 페이지 번호를 가져옵니다. 기본값은 1입니다.
    search_field = request.GET.get('search_field', '')  # 검색 필드를 가져옵니다. search_field라는 이름으로 GET 요청에서 검색 필드를 가져옵니다.
    user = event_member.objects.get(mem_idx=user_idx)  # user_idx에 해당하는 event_member 객체를 가져옵니다.
    if request.method == 'POST':
        
        user.mem_id = request.POST.get('mem_id')
        user.mem_name = request.POST.get('mem_name')
        user.mem_HP = request.POST.get('mem_HP')
        mem_email = request.POST.get('mem_email')
        if mem_email:
            if '@' in mem_email:
                arr_email = mem_email.split('@')
                user.mem_email1=arr_email[0]
                user.mem_email2=arr_email[1]
        user.mem_Event = request.POST.get('mem_Event')
        mem_YN = request.POST.get('mem_YN')
        if mem_YN == 'Y':
            user.mem_YN = 'Y'
        elif mem_YN == 'P':
            user.mem_YN = 'P'
        elif mem_YN == 'N':
            user.mem_YN = 'N'
        user.save()  # 변경된 정보를 저장합니다.
        return redirect(reverse('user_member:user_detail', args=[user_idx]) + f'?page={page}&kw={kw}&search_field={search_field}')  # 회원 상세 페이지로 리디렉션합니다.
    else:
        return render(request, 'livemanager/user_member/member_update.html', {'user': user, 'kw': kw, 'page': page, 'search_field': search_field})  

@login_required(login_url='adminUser:admin_login')  # 로그인하지 않은 경우 admin_login 페이지로 리다이렉트
def user_detail(request, user_idx, kw='', page=1, search_field=''):
    kw = request.GET.get('kw', '')  # 검색어를 가져옵니다. kw라는 이름으로 GET 요청에서 검색어를 가져옵니다.
    page = request.GET.get('page', 1)  # 페이지 번호를 가져옵니다. 기본값은 1입니다.
    search_field = request.GET.get('search_field', '')  # 검색 필드를 가져옵니다. search_field라는 이름으로 GET 요청에서 검색 필드를 가져옵니다.
    
    user = event_member.objects.get(mem_idx=user_idx)  # user_idx에 해당하는 event_member 객체를 가져옵니다.
    return render(request, 'livemanager/user_member/member_detail.html', {'user': user, 'user_idx': user_idx, 'kw': kw, 'page': page, 'search_field': search_field})

@login_required(login_url='adminUser:admin_login')  # 로그인하지 않은 경우 admin_login 페이지로 리다이렉트
def user_excel_create(request):
    return render(request, 'livemanager/user_member/member_excel_create.html')


@login_required(login_url='adminUser:admin_login')  # 로그인하지 않은 경우 admin_login 페이지로 리다이렉트
def user_delete(request, user_idx, kw='', page=1, search_field=''):
    user = event_member.objects.get(mem_idx=user_idx)  # user_idx에 해당하는 event_member 객체를 가져옵니다.
    user.delete()  # 해당 회원 객체를 삭제합니다.
    return redirect(reverse('user_member:user_list') + f'?page={page}&kw={kw}&search_field={search_field}')  # 회원 목록 페이지로 리디렉션합니다.