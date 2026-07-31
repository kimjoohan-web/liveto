import json

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from httpx import request
from .models import Answer, Choice, LiveStream, Question
from .forms import QuestionForm, ChoiceFormSet

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import connection

# Create your views here.

def index(request):
    if 'mem_name' not in request.session:
        return redirect('member:mem_login')  # 로그인 페이지로 리디렉션
    stream = LiveStream.objects.filter(is_live=True).first()
    return render(request, 'livepoll/index.html', {'stream': stream})


def create_poll(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)


        
        if question_form.is_valid():
            if question_form.cleaned_data['is_voting_now']==True:
                # 현재 투표 진행 상태를 False로 초기화
                live_stream_id = question_form.cleaned_data['live_stream'].id
                Question.objects.filter(live_stream_id=live_stream_id).update(is_voting_now=False)

            # 주관식(TEXT)일 때는 보기를 검증/저장하지 않아도 됨
            if question_form.cleaned_data['question_type'] == 'TEXT':
                question_form.save()
                return redirect('livepoll:livepoll_list') # 이동할 페이지 주소
            
            # 객관식일 때는 폼셋까지 모두 유효해야 저장
            if formset.is_valid():
                question = question_form.save()
                choices = formset.save(commit=False)
                for choice in choices:
                    choice.question = question
                    choice.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
                f'live_poll_{question.live_stream.id}',  # Consumer에서 지정한 그룹명
                {
                    'type': 'poll_update_message'  # Consumer의 메서드명 (점 대신 언더바)
                }
        )


        return redirect('livepoll:livepoll_list')
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()
        
    return render(request, 'livepoll/create_poll.html', {
        'question_form': question_form,
        'formset': formset,
    })

@login_required(login_url='adminUser:admin_login')
def livepoll_list(request):
    questions = Question.objects.all().order_by('-created_at')
    choices = {question.id: question.choices.all() for question in questions}    

    return render(request, 'livepoll/livepoll_list.html', {'questions': questions, 'choices': choices})

def modify_poll(request, question_id):
    # print(f"modify_poll called with question_id: {question_id}")  # 디버깅용 출력
    print(f"Request method: {request.method}")  # 디버깅용 출력

    question = get_object_or_404(Question, id=question_id)     
    

  

    if request.method == 'POST':
        live_stream = request.POST['live_stream']
        question_text = request.POST['question_text']
        question_type = request.POST['question_type']
        is_voting_now = 'is_voting_now' in request.POST  # 체크박스 처리

        # 먼저 live_stream_id 의 is_voting_now 상태를 False로 초기화
        sql_reset_voting = f"UPDATE livepoll_question SET is_voting_now=FALSE WHERE live_stream_id={live_stream};"
        print(f"SQL Reset Voting Query: {sql_reset_voting}")  # 디버깅용
        with connection.cursor() as cursor:
            cursor.execute(sql_reset_voting)


        # sql_status_check = f"SELECT is_voting_now FROM livepoll_question WHERE id={question_id} LIMIT 1;"
        # with connection.cursor() as cursor:
        #     cursor.execute(sql_status_check)
        #     current_status = cursor.fetchone()[0]

        # if current_status==False:
        #     is_voting_now = True  # 현재 투표 진행 중이면 해제
        # else:
        #     is_voting_now = False  # 현재 투표 진행 중이 아니면 진행 상태로 변경

        sql_modify = f"UPDATE livepoll_question SET live_stream_id={live_stream}, question_text='{question_text}', question_type='{question_type}', is_voting_now={is_voting_now} WHERE id={question_id};"
        print(f"SQL Modify Query: {sql_modify}")  # 디버깅용
        with connection.cursor() as cursor:
            cursor.execute(sql_modify)


        sql_delete_choices = f"DELETE FROM livepoll_choice WHERE question_id={question_id};"
        print(f"SQL Delete Choices Query: {sql_delete_choices}")  # 디버깅용
        with connection.cursor() as cursor:
            cursor.execute(sql_delete_choices)


       

            # 해당 보기를 받아온다. 
        print(f"Request question_type data: {request.POST['question_type']}")  # 디버깅용 출력
        print(f"Request choices data1: {request.POST.getlist('choice_text')}")  # 디버깅용 출력
        

        if request.POST['question_type'] == 'SINGLE' or request.POST['question_type'] == 'MULTIPLE':
                choices_options = []
                for key,value in request.POST.items():
                    if key.startswith('choices-') and key.endswith('-choice_text'):
                        if value.strip():  # 공백이 아닌 경우에만 추가
                            choices_options.append(value)


                print(f"Request choices data2: {choices_options}")  # 디버깅용 출력
                for choice_text in choices_options: 
                    sql_insert_choice = f"INSERT INTO livepoll_choice (question_id, choice_text, votes_count) VALUES ({question_id}, '{choice_text}', 0);"
                    print(f"SQL Insert Choice Query: {sql_insert_choice}")  # 디버깅용
                    with connection.cursor() as cursor:
                        cursor.execute(sql_insert_choice) 


                # -------------------------------------------------------------
                # 🚀 WebSocket 이벤트 발송
                # -------------------------------------------------------------
                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                            f'live_poll_{question.live_stream.id}',  # Consumer에서 지정한 그룹명
                            {
                                'type': 'poll_update_message'  # Consumer의 메서드명 (점 대신 언더바)
                            }
                    )
                        
        return redirect('livepoll:livepoll_list')
    
    else:
        
        question_form = QuestionForm(instance=question)
        formset = ChoiceFormSet(instance=question)
        answers = Answer.objects.filter(question=question)
        # 답변한 내역이 존재한다면 
        
    
    return render(request, 'livepoll/modify_poll.html', {
        'question_form': question_form,
        'formset': formset,
        'question_id': question_id,
        'answers': answers,
    })

def delete_poll(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('livepoll:livepoll_list')



def go_poll(request, question_id):

#request.session['mem_name'] = member[1]  저장된 값 불러오기 seession  값 유무 확인 
    if 'mem_name' not in request.session:
        return redirect('member:mem_login')  # 로그인 페이지로 리디렉션

    question = get_object_or_404(Question, id=question_id)

    # 먼저 live_stream_id 의 is_voting_now 상태를 False로 초기화
    Question.objects.filter(live_stream_id=question.live_stream.id).update(is_voting_now=False)
    # 그 다음 현재 선택된 question의 is_voting_now 상태를 True로 설정    
    is_voting_now = question.is_voting_now 
    if is_voting_now == False:
        question.is_voting_now = True  # 투표 진행 상태로 변경
    else:
        question.is_voting_now = False  # 투표 진행 상태를 해제

    question.save()
    
    # WebSocket을 통해 실시간으로 투표 진행 상태를 알림
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'live_poll_{question.live_stream.id}',  # Consumer에서 지정한 그룹명
        {
            'type': 'poll_update_message',  # Consumer의 메서드명 (점 대신 언더바)
            'action': 'start_poll',
            'poll_id': question.id,
            'question': question.question_text,
        }
    )
    
    return redirect('livepoll:livepoll_list')
# views.py 예시
def create_livestream(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        stream_url = request.POST.get('stream_url')
        
        # 체크박스는 체크 해제 시 request.POST에 'is_live' 키가 넘어오지 않으므로 아래처럼 처리
        is_live = 'is_live' in request.POST  # True 또는 False 반환
        
        LiveStream.objects.create(
            title=title,
            stream_url=stream_url,
            is_live=is_live
        )
        return redirect('livepoll:livestream_list')
    return render(request, 'livepoll/create_livestream.html')



def livestream_list(request):
    streams = LiveStream.objects.all()
    return render(request, 'livepoll/livestream_list.html', {'streams': streams})


def stream_view(request, stream_id):
    stream = LiveStream.objects.get(id=stream_id)
    return render(request, 'livepoll/stream_view.html', {'stream': stream})

def modify_livestream(request, stream_id):
    stream = LiveStream.objects.get(id=stream_id)
    
    if request.method == 'POST':
        stream.title = request.POST.get('title')
        stream.stream_url = request.POST.get('stream_url')
        stream.is_live = 'is_live' in request.POST  # 체크박스 처리
        stream.save()
        return redirect('livepoll:livestream_list')
    
    return render(request, 'livepoll/modify_livestream.html', {'stream_view': stream})




def submit_vote(request, question_id):
    if 'mem_name' not in request.session:
        return redirect('member:mem_login')  # 로그인 페이지로 리디렉션
    user_id=request.session.get('mem_name')  # 세션에서 사용자 ID 가져오기
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        qType = question.question_type
        print(f"submit_vote called with question_id: {question_id}, question_type: {qType}")  # 디버깅용 출력
        data = json.loads(request.body)
        selected_choices = []
        answer_text = ''
        if qType in['SINGLE', 'MULTIPLE']:
            # selected_choices = request.POST.getlist('choices')
            selected_choices = data.get('choices', [])
            print(f"Selected choices: {selected_choices}")  # 디버깅용 출력
        
        elif qType == 'TEXT':
            answer_text = data.get('answer_text', '').strip()
            print(f"Answer text: {answer_text}")  # 디버깅용 출력
        # 투표 처리 로직 호출
        process_poll(question_id, selected_choices if qType in ['SINGLE', 'MULTIPLE'] else [], answer_text if qType == 'TEXT' else None, user_id)

        # WebSocket을 통해 실시간으로 투표 결과를 알림
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'live_poll_{question.live_stream.id}',  # Consumer에서 지정한 그룹명
            {
                'type': 'update_results',  # Consumer의 메서드명 (점 대신 언더바)
                'action': 'vote_submitted',
                'question_id': question.id,
                'selected_choices': selected_choices,
                'answer_text': answer_text if qType == 'TEXT' else '',
            }
        )

        return redirect('livepoll:livepoll_list')
    else:
        return redirect('livepoll:go_poll', question_id=question_id)

def process_poll(question_id, selected_choices, answer_text, user):
    question = Question.objects.get(id=question_id)
    answer = Answer.objects.create(
        user=user,
        question=question,
        answer_text=answer_text if question.question_type == 'TEXT' else None
    )
    if question.question_type in ['SINGLE', 'MULTIPLE']:
        choices = Choice.objects.filter(id__in=selected_choices)
        answer.selected_choices.set(choices)
        for choice in choices:
            choice.votes_count += 1
            choice.save()
       
       