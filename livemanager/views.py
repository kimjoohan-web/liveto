from urllib import response,request

from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.utils import timezone


import pandas as pd
#mssql 연결문자



# mssql_str = f"DRIVER={settings.DATABASES['mssql_db']['OPTIONS']['driver']};SERVER={settings.DATABASES['mssql_db']['HOST']};DATABASE={settings.DATABASES['mssql_db']['NAME']};UID={settings.DATABASES['mssql_db']['USER']};PWD={settings.DATABASES['mssql_db']['PASSWORD']};Encrypt={settings.DATABASES['mssql_db']['OPTIONS']['encrypt']};"
       
    
# Create your views here.

def login_required_view(view_func):# 로그인 여부 확인 데코레이터
    def wrapper(request, *args, **kwargs):
        if not request.session.get('mem_name'):
            return redirect('livemanager:mem_login', next=request.path)  # 로그인 페이지로 리다이렉트
        return view_func(request, *args, **kwargs)
    return wrapper



def index(request):    
    if not request.session.get('mem_name'):
        return redirect('livemanager:mem_login')  # 로그인 페이지로 리다이렉트
    # mssql 연결
    page = request.GET.get('page', '1')  # 페이지   # 페이지 번호, 기본값은 1
    kw = request.GET.get('kw', '')  # 검색어, 기본값은 빈 문자열
    
    page_obj = None

    # mssql_conn = pyodbc.connect(mssql_str)
    # cursor = mssql_conn.cursor()
    # # SQL 쿼리 실행
    # sql_str = "SELECT top 100 * FROM event_member order by mem_idx desc"  # 실제 테이블 이름으로 변경
    # cursor.execute(sql_str)  # 실제 테이블 이름으로 변경
    # rows = cursor.fetchall()

    
    
    # # 결과를 리스트로 변환
    # # data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    # paginator_1 = Paginator(rows,int(10))  # 페이지당 10개씩 보여주기  
    # page_obj = paginator_1.get_page(page)  
    # context ={'members':page_obj,'page':page,'kw':kw}

    # 
    
    sql_str = "SELECT case when mem_yn='N' then '승인안됨' else '승인됨' end as status,    * FROM event_member  "  # 실제 테이블 이름으로 변
    if kw:
        sql_str += f"WHERE mem_name LIKE '%{kw}%' OR mem_id LIKE '%{kw}%' "   # 검색어가 있는 경우에만 WHERE 절 추가
    else:
        sql_str += f"WHERE 1=1 "  # 검색어가 없는 경우에도 WHERE 절을 추가하여 기본적으로 모든 데이터를 조회하도록 함

    sql_str += f"order by mem_idx desc "  # 페이지네이션을 위한 LIMIT 절 추가

    with connection.cursor() as cursor:
        cursor.execute(sql_str)  # 실제 테이블 이름으로 변경
        rows = cursor.fetchall()


  
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]


    paginator_1 = Paginator(data,int(10))  # 페이지당 10개씩 보여주기  
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

        
        
        sql_str = f"INSERT INTO event_member ("
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
        sql_str += f", '{timezone.now()}'"
        sql_str += f", '{Country}')"
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_str)
                connection.commit()
            # return redirect('livemanager:index')  # 회원 가입 후 리다이렉트할 URL 이름
            return redirect('board:index')  # 회원 가입 후 리다이렉트할 URL 이름
        except Exception as e:
            print(f"Error executing SQL: {e}")
            # 에러 처리 (예: 사용자에게 에러 메시지 표시)
            return render(request, 'livemanager/member/member_input.html', {'error': '데이터 저장 중 오류가 발생했습니다.'})
        


        # 예: name = request.POST.get('name')
        #     email = request.POST.get('email')
        #     ... (다른 필드들도 처리)
        
        # 데이터베이스에 저장하거나 필요한 작업 수행
        # 예: Member.objects.create(name=name, email=email, ...)
        
        # 처리 후 리다이렉트 또는 성공 메시지 반환
        
    else:    
        return render(request, 'livemanager/member/member_input.html')
    
def mem_login(request, next=None):
    if request.method == 'POST':
        mem_name = request.POST.get('mem_name')
        mem_HP = request.POST.get('mem_HP')
        
        sql_str = f"SELECT mem_idx,mem_name,mem_HP,concat(mem_email1,'@',mem_email2) as mem_email  FROM event_member WHERE mem_name='{mem_name}' and mem_HP='{mem_HP}'"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)  # 실제 테이블 이름으로 변경
            row = cursor.fetchone()
            
        if row is not None:
            request.session['mem_name'] = row[1]  # 세션에 mem_name 저장
            request.session['mem_HP'] = row[2]  # 세션에 mem_HP 저장
            request.session['mem_email'] = row[3]  # 세션에 mem_email 저장
            # 로그인 성공
            if next:
                return redirect(next)  # 로그인 후 원래 요청한 URL로 리다이렉트
            return redirect('livemanager:index')  # 로그인 후 리다이렉트할 URL 이름
        else:
            # 로그인 실패
            return render(request, 'livemanager/member/login.html', {'messages': '로그인 정보가 올바르지 않습니다.'})
    else:
        return render(request, 'livemanager/member/login.html') 


def member_modify(request, mem_idx):   

    if not request.session.get('mem_name'):
        return redirect('livemanager:mem_login')  # 로그인 페이지로 리다이렉트
    

    
    mem_idx = int(mem_idx)  # mem_idx를 정수로 변환
    member_data = None  # 초기화
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

        
        
        sql_str = f"UPDATE event_member SET "
        sql_str += f" mem_name='{mem_name}'"
        sql_str += f", mem_HP='{mem_HP}'"
        sql_str += f", mem_email1='{mem_email1}'"
        sql_str += f", mem_email2='{mem_email2}'"
        sql_str += f", mem_hospital='{mem_hospital}'"
        sql_str += f", mem_dept='{mem_dept}'"
        sql_str += f", Country='{Country}'"
        sql_str += f" WHERE mem_idx={mem_idx}"
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_str)
                connection.commit()
            return redirect('livemanager:index')  # 회원 수정 후 리다이렉트할 URL 이름
        except Exception as e:
            print(f"Error executing SQL: {e}")
            # 에러 처리 (예: 사용자에게 에러 메시지 표시)
            return render(request, 'livemanager/member/member_modify.html', {'error': '데이터 저장 중 오류가 발생했습니다.'})
        


    else:    
        
        
        sql_str = f"SELECT concat(mem_email1,'@',mem_email2) as mem_email, * FROM event_member WHERE mem_idx=%s"  # 실제 테이블 이름으로 변경

        with connection.cursor() as cursor:
            cursor.execute(sql_str, [mem_idx])  # 실제 테이블 이름으로 변경
            row = cursor.fetchone()
            if row is not None:
                member_data = dict(zip([column[0] for column in cursor.description], row))
       

        context = {'member': member_data}
        return render(request, 'livemanager/member/member_modify.html', context)    
    

def member_delete(request, mem_idx):
    mem_idx = int(mem_idx)  # mem_idx를 정수로 변환
    sql_str = f"DELETE FROM event_member WHERE mem_idx={mem_idx}"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            connection.commit()
        return redirect('livemanager:index')  # 회원 삭제 후 리다이렉트할 URL 이름
    except Exception as e:
        print(f"Error executing SQL: {e}")
        # 에러 처리 (예: 사용자에게 에러 메시지 표시)
        return render(request, 'livemanager/member/member_list.html', {'error': '데이터 삭제 중 오류가 발생했습니다.'})         
        

def member_excel_download(request):
    # 엑셀 다운로드 기능 구현
    # 예: 데이터를 조회하여 엑셀 파일로 생성 후 다운로드 링크 제공
    kw = request.GET.get('kw', '')  # 검색어 가져오기
    sql_str = "SELECT case when mem_yn='N' then '승인안됨' else '승인됨' end as status,    mem_idx"
    sql_str += " ,mem_event"
    sql_str += " ,mem_id"
    sql_str += " ,mem_name"
    sql_str += " ,mem_HP"
    sql_str += " ,mem_email1"
    sql_str += " ,mem_email2"
    sql_str += " ,mem_hospital"
    sql_str += " ,mem_input_date"
    sql_str += " ,status FROM event_member  "  # 실제 테이블 이름으로 변
    
    if kw:
        sql_str += f"WHERE mem_name LIKE '%{kw}%' OR mem_id LIKE '%{kw}%' "   # 검색어가 있는 경우에만 WHERE 절 추가
    else:
        sql_str += f"WHERE 1=1 "  # 검색어가 없는 경우에도 WHERE 절을 추가하여 기본적으로 모든 데이터를 조회하도록 함

    sql_str += f"order by mem_idx desc "  # 페이지네이션을 위한 LIMIT 절 추가

    with connection.cursor() as cursor:
        cursor.execute(sql_str)  # 실제 테이블 이름으로 변경
        rows = cursor.fetchall()

    #엑셀 파일 생성 및 다운로드 처리
    # data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    data = list(rows)  # 튜플을 리스트로 변환    
    df = pd.DataFrame(data)
    excel_file_path = 'members.xlsx'  # 엑셀 파일 경로 설정
    respnose = HttpResponse(content_type='application/vnd.ms-excel')
    respnose['Content-Disposition'] = 'attachment; filename='+excel_file_path
    
    df.to_excel(respnose, index=False)  # 엑셀 파일로 저장
    
    return respnose
    


def member_excel_upload(request):
    if request.method == 'POST':
        # 엑셀 파일 업로드 처리
        excel_file = request.FILES['excel_file']
        if excel_file:
            # 엑셀 파일을 읽어서 데이터베이스에 저장하는 로직 구현
            # 예: pandas를 사용하여 엑셀 파일 읽기
            df = pd.read_excel(excel_file)  # 엑셀 파일의 첫 번째 시트를 읽음
            # 데이터프레임을 순회하면서 데이터베이스에 저장하는 로직 구현
            for index, row in df.iterrows():  # 첫 번째 행은 헤더이므로 2부터 시작        
                mem_name = row['mem_name']
                mem_HP = row['mem_HP']
                mem_email_arr = []
                mem_email = row['mem_email']
                if mem_email: # @가 포함된 이메일이 입력된 경우에만 분리
                    if '@' in mem_email:
                        mem_email_arr = mem_email.split('@')  # 이메일 @ 기준으로 분리
                        mem_email1 = mem_email_arr[0]  # @ 앞 부분
                        mem_email2 = mem_email_arr[1]  # @ 뒤 부분

                mem_hospital = row['mem_hospital']
                mem_depart = row['mem_depart']
                dc_licence = row['dc_licence']
                work_id = row['work_id']
                mem_duty = row['mem_duty']
                mem_SalesName = row['mem_SalesName']              
                mem_teamName = row['mem_teamName']
                mem_address1 = row['mem_address1']
                mem_address2 = row['mem_address2']
                mem_Event = row['mem_Event']
                event_gubun = row['event_gubun']
                mem_YN = row['mem_YN']
                Country =""
               
                #엑셀 입력전에  중복체크
                sql_str_exit = f"SELECT mem_idx FROM event_member WHERE mem_HP='{mem_HP}' and mem_event='{mem_Event}'"
                with connection.cursor() as cursor:
                    cursor.execute(sql_str_exit)  # 실제 테이블 이름으로 변경
                    row = cursor.fetchone()
                    
                if row is None: # 중복된 데이터가 없는 경우에만 삽입
                        
                        sql_str = f"INSERT INTO event_member ("
                        sql_str += f" mem_id"
                        sql_str += f" ,mem_name"
                        sql_str += f", mem_HP "
                        sql_str += f", mem_email1"
                        sql_str += f", mem_email2"
                        sql_str += f", mem_hospital"
                        sql_str += f", mem_depart"
                        sql_str += f", mem_Event"
                        sql_str += f", event_gubun"
                        sql_str += f", mem_YN"
                        sql_str += f", mem_address1"
                        sql_str += f", mem_address2"
                        sql_str += f", dc_licence"
                        sql_str += f", work_id"
                        sql_str += f", mem_duty"
                        sql_str += f", mem_teamName"
                        sql_str += f", mem_SalesName"
                        sql_str += f", mem_input_date"
                        sql_str += f", Country) VALUES "
                        sql_str += f"('{mem_HP}'"
                        sql_str += f", '{mem_name}'"
                        sql_str += f", '{mem_HP}'"
                        sql_str += f", '{mem_email1}'"
                        sql_str += f", '{mem_email2}'"
                        sql_str += f", '{mem_hospital}'"
                        sql_str += f", '{mem_depart}'"
                        sql_str += f",  {mem_Event}"
                        sql_str += f", '{event_gubun}'"
                        sql_str += f", '{mem_YN}'"
                        sql_str += f", '{mem_address1}'"
                        sql_str += f", '{mem_address2}'"
                        sql_str += f", '{dc_licence}'"
                        sql_str += f", '{work_id}'"
                        sql_str += f", '{mem_duty}'"
                        sql_str += f", '{mem_teamName}'"
                        sql_str += f", '{mem_SalesName}'"
                        # sql_str += f", NOW()"
                        sql_str += f", '{timezone.now()}'"
                        sql_str += f", '{Country}')"
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(sql_str)
                                connection.commit()
                        except Exception as e:
                            print(f"Error executing SQL: {e}")
                            # 에러 처리 (예: 사용자에게 에러 메시지 표시)
                            # return render(request, 'livemanager/member/member_list.html', {'error': '데이터 삽입 중 오류가 발생했습니다.'})
                            return redirect('livemanager:index',{'error': f'데이터 삽입 중 {e} 오류가 발생했습니다.'})  # 엑셀 업로드 후 리다이렉트할 URL 이름
                else:
                    continue # 중복된 데이터가 있는 경우에는 건너뛰기


        return redirect('livemanager:index')  # 엑셀 업로드 후 리다이렉트할 URL 이름
    else:
        return render(request, 'livemanager/member/member_excel_upload.html')
                
        
def member_bulk_delete(request):
   
        mem_idx_list = request.GET.getlist('mem_idx_list')  # 선택된 회원의 mem_idx 리스트 가져오기
        if mem_idx_list:
            mem_idx_str = ','.join(mem_idx_list)  # mem_idx 리스트를 문자열로 변환
            sql_str = f"DELETE FROM event_member WHERE mem_idx IN ({mem_idx_str})"
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql_str)
                    connection.commit()
                return redirect('livemanager:index')  # 회원 삭제 후 리다이렉트할 URL 이름
            except Exception as e:
                print(f"Error executing SQL: {e}")
                return redirect('livemanager:index',{'error': f'데이터 삭제 중 {e} 오류가 발생했습니다.'})  # 회원 삭제 후 리다이렉트할 URL 이름
        else:
            return redirect('livemanager:index',{'error': '선택된 회원이 없습니다.'})  # 회원 삭제 후 리다이렉트할 URL 이름
   

def member_logout(request):
    request.session.flush()  # 세션 데이터 삭제
    return redirect('livemanager:index')  # 로그아웃 후 리다이렉트할 URL 이름