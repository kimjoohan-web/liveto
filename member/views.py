
from django.utils import timezone
from sys import path

from django.shortcuts import redirect, render
from board import views
from django.db import connection

# # Create your views here.
# def index(request):
#     return render(request, 'member/index.html')

def index(request):
    redirect_url = 'board:index'  # 리디렉션할 URL 이름
    return redirect(redirect_url)
    

def member_input(request):

    if request.method == 'POST':
        # POST 요청 처리
        
        mem_name = request.POST.get('mem_name')
        mem_hospital = request.POST.get('mem_hospital')
        mem_dept = request.POST.get('mem_dept')            
        mem_email = request.POST.get('mem_email')        
        mem_country = request.POST.get('Country')
        mem_HP = request.POST.get('mem_HP')
        mem_email= request.POST.get('mem_email')
        if mem_email:
            arr_email =[]
            if '@' in mem_email:
                arr_email = mem_email.split('@')
                mem_email1 = arr_email[0]
                mem_email2 = arr_email[1]
          
        mem_Event = 0
            

        strsql = "INSERT INTO event_member (mem_id, mem_name, mem_dept,  mem_email1, mem_email2,  Country, mem_HP, mem_hospital, mem_input_date, mem_Event) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (mem_HP, mem_name, mem_dept, mem_email1, mem_email2, mem_country, mem_HP, mem_hospital, timezone.now(), mem_Event)
        with connection.cursor() as cursor:
            cursor.execute(strsql, params)
            connection.commit()        

        # 처리 후 리디렉션 또는 다른 페이지로 이동
        return redirect('board:index')  # 예: 회원 목록 페이지로 리디렉션
    
    else:
        # GET 요청 처리 (회원 입력 폼 표시)
        return render(request, 'member/member_input.html')  
    


def member_modify(request, mem_idx):
    if request.method == 'POST':
        # POST 요청 처리
        mem_name = request.POST.get('mem_name')
        mem_dept = request.POST.get('mem_dept')
        
        mem_email = request.POST.get('mem_email')
        mem_email1 = ''
        mem_email2 = ''
        if mem_email:
            if '@' in mem_email:
                arr_email = mem_email.split('@')
                mem_email1 = arr_email[0]
                mem_email2 = arr_email[1]

        
        mem_country = request.POST.get('Country')
        mem_HP = request.POST.get('mem_HP')
        mem_hospital = request.POST.get('mem_hospital')
        

        strsql = "UPDATE event_member SET mem_name=%s, mem_dept=%s, mem_email1=%s, mem_email2=%s, Country=%s, mem_HP=%s, mem_hospital=%s WHERE mem_idx=%s"
        params = (mem_name, mem_dept, mem_email1, mem_email2, mem_country, mem_HP, mem_hospital, mem_idx)
        with connection.cursor() as cursor:
            cursor.execute(strsql, params)
            connection.commit()

        # 처리 후 리디렉션 또는 다른 페이지로 이동
        return redirect('board:index')  # 예: 회원 목록 페이지로 리디렉션
    else:
        # GET 요청 처리 (회원 수정 폼 표시)
        strsql = "SELECT mem_idx, mem_name, mem_dept, concat(mem_email1,'@',mem_email2) as mem_email, Country, mem_HP, mem_hospital FROM event_member WHERE mem_idx=%s"
        
        with connection.cursor() as cursor:
            cursor.execute(strsql, (mem_idx,))
            member = cursor.fetchone()

        data = dict(zip([column[0] for column in cursor.description], member)) if member else None

        return render(request, 'member/member_modify.html', {'member': data, 'mem_idx': mem_idx})  # 예: 회원 수정 폼 페이지로 이동
    
    

def member_delete(request, mem_idx):
    if request.method == 'POST':
        # POST 요청 처리
        strsql = "DELETE FROM event_member WHERE mem_idx=%s"
        params = (mem_idx,)
        with connection.cursor() as cursor:
            cursor.execute(strsql, params)
            connection.commit()

        # 처리 후 리디렉션 또는 다른 페이지로 이동
        return redirect('board:index')  # 예: 회원 목록 페이지로 리디렉션 
    


def mem_login(request):
    if request.method == 'POST':
        mem_name = request.POST.get('mem_name')
        mem_HP = request.POST.get('mem_HP')

        # 데이터베이스에서 회원 정보 조회
        strsql = "SELECT mem_idx, mem_name, mem_HP FROM event_member WHERE mem_name=%s AND mem_HP=%s"
        params = (mem_name, mem_HP)
        with connection.cursor() as cursor:
            cursor.execute(strsql, params)
            member = cursor.fetchone()

        if member:
            # 로그인 성공 시 세션에 회원 정보 저장
            request.session['mem_idx'] = member[0]  # 예: 회원 인덱스
            request.session['mem_name'] = member[1]  # 예: 회원 이름
            request.session['mem_HP'] = member[2]  # 예: 회원 전화번호
            request.session['mem_id'] = member[2]  # 예: 회원 ID
            # 필요한 다른 정보도 세션에 저장 가능

            return redirect('board:index')  # 로그인 성공 후 리디렉션할 URL
        else:
            # 로그인 실패 시 에러 메시지 전달
            error_message = "이름 또는 전화번호가 올바르지 않습니다."
            return render(request, 'member/mem_login.html', {'error_message': error_message})
    else:
        # GET 요청 처리 (로그인 폼 표시)
        return render(request, 'member/mem_login.html')


def member_logout(request):
    # 로그아웃 처리 로직 작성 (예: 세션 종료, 쿠키 삭제 등)
    # 예시로 세션을 종료하는 경우:
    request.session.flush()  # 모든 세션 데이터 삭제

    # 로그아웃 후 리디렉션할 URL로 이동
    return redirect('board:index')  # 예: 홈 페이지로 리디렉션


    

