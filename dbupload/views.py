from turtle import pd
from django.shortcuts import redirect, render
from django.db import connection
from django.utils import timezone



# Create your views here.
def index(request):
    return render(request, 'dbupload/index.html')

def db_excel_upload(request):
    if request.method == 'POST':       
        excel_file = request.FILES.get('excel_file')

        # 테이블 이름과 엑셀 파일이 모두 제공되었는지 확인
        if not excel_file:
            error_message = "엑셀 파일을 제공해야 합니다."
            return render(request, 'dbupload/index.html', {'error': error_message})


        
        if excel_file:
            # 엑셀 파일을 읽어서 데이터베이스에 저장하는 로직 구현
            # 예: pandas를 사용하여 엑셀 파일 읽기
            df = pd.read_csv(excel_file)  # 엑셀 파일의 첫 번째 시트를 읽음
            # 데이터프레임을 순회하면서 데이터베이스에 저장하는 로직 구현
            for index, row in df.iterrows():  # 첫 번째 행은 헤더이므로 2부터 시작        
                    car_idx = row['car_idx']
                    car_name = row['car_name']
                    car_order = row['car_order']
                    car_field = row['car_field']
                    car_year = row['car_year']
                    car_day = row['car_day']
                    car_date = row['car_date']
                    car_url = row['car_url']
                    car_size_h = row['car_size_h']
                    car_size_w = row['car_size_w']
                    car_check = row['car_check']
                    car_readnum = row['car_readnum']
                    car_content = row['car_content']
                    car_image = row['car_image']
                    car_choo = row['car_choo']
                    car_soonwe = row['car_soonwe']
                        
                    sql_str = f"INSERT INTO board ("
                    sql_str += f" car_idx"
                    sql_str += f" ,car_name"
                    sql_str += f", car_order "
                    sql_str += f", car_field"
                    sql_str += f", car_year"
                    sql_str += f", car_day"
                    sql_str += f", car_date"
                    sql_str += f", car_url"

                    sql_str += f", car_size_h"
                    sql_str += f", car_size_w"
                    sql_str += f", car_check"
                    sql_str += f", car_readnum"
                    sql_str += f", car_content"
                    sql_str += f", car_image"
                    sql_str += f", car_choo"
                    sql_str += f", car_soonwe ) values ("
                    sql_str += f"('{car_idx}'"
                    sql_str += f", '{car_name}'"
                    sql_str += f", '{car_order}'"
                    sql_str += f", '{car_field}'"
                    sql_str += f", '{car_year}'"
                    sql_str += f", '{car_day}'"
                    sql_str += f", '{car_date}'"
                    sql_str += f", '{car_url}'"     
                    sql_str += f", '{car_size_h}'"
                    sql_str += f", '{car_size_w}'"
                    sql_str += f", '{car_check}'"
                    sql_str += f", '{car_readnum}'"
                    sql_str += f", '{car_content}'"
                    sql_str += f", '{car_image}'"
                    sql_str += f", '{car_choo}'"
                    sql_str += f", '{car_soonwe}')"


                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(sql_str)
                            connection.commit()
                    except Exception as e:
                        print(f"Error executing SQL: {e}")
                        # 에러 처리 (예: 사용자에게 에러 메시지 표시)
                        # return render(request, 'livemanager/member/member_list.html', {'error': '데이터 삽입 중 오류가 발생했습니다.'})
                        return redirect('dbupload:index',{'error': f'데이터 삽입 중 {e} 오류가 발생했습니다.'})  # 엑셀 업로드 후 리다이렉트할 URL 이름
        return redirect('dbupload:index')  # 엑셀 업로드 후 리다이렉트할 URL 이름
    else:
        return render(request, 'dbupload/index.html')
    



        # 엑셀 파일 처리 로직 추가 (예: 데이터베이스에 업로드)
        # 여기서 엑셀 파일을 읽고, 지정된 테이블에 데이터를 삽입하는 로직을 구현해야 합니다.
        # 예를 들어 pandas를 사용하여 엑셀 파일을 읽고, Django ORM을 사용하여 데이터를 삽입할 수 있습니다.

        # 성공적으로 업로드 후 리다이렉트 또는 성공 메시지 표시
        success_message = "엑셀 파일이 성공적으로 업로드되었습니다."
        return render(request, 'dbupload/index.html', {'success': success_message})

    return render(request, 'dbupload/index.html')


    