# polls/consumers.py
import json
from math import pi
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        print(f"Stream ID from URL: {self.stream_id}")  # 디버깅용  
        self.room_group_name = f'live_poll_{self.stream_id}'

        print(f"Connecting to room group: {self.room_group_name}")  # 디버깅용

        # 사용자를 해당 라이브 방송방(Group)에 참여시킴
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_poll_question()
        # await self.get_current_question()

    async def send_poll_question(self):
        question_data = await self.get_current_question()
        if question_data:
            await self.send(text_data=json.dumps({
                'type': 'NEW_QUESTION',
                'question_id': question_data['question_id'],
                'text': question_data['text'],
                'q_type': question_data['q_type'],
                'choices': question_data['choices']
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'NO_QUESTION'
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 1. 관리자가 새 질문을 전송했을 때 유저들에게 브로드캐스팅
    async def send_question(self, event):
        await self.send(text_data=json.dumps({
            'type': 'NEW_QUESTION',
            'question_id': event['question_id'],
            'text': event['text'],
            'q_type': event['q_type'],
            'choices': event['choices'] # 보기 목록 리스트
        }))

    # 2. 누군가 투표를 해서 결과가 업데이트되었을 때 브로드캐스팅
    async def update_results(self, event):
        poll_results = await self.poll_result(event['question_id'])
        await self.send(text_data=json.dumps({
            'type': 'POLL_RESULT',
            'question_id': event['question_id'],
            'results': poll_results # 득표 현황 및 주관식 답변 목록 데이터
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('type')

        if action == 'SUBMIT_VOTE':
            question_id = data.get('question_id')
            selected_choices = data.get('choices', [])
            answer_text = data.get('answer_text', '')

            # 투표 처리 로직 호출
            await self.process_poll(question_id, selected_choices, answer_text)
    
    @database_sync_to_async
    def get_current_question(self):
        from .models import Question
        try:
            question = Question.objects.filter(live_stream_id=self.stream_id, is_voting_now=True).order_by('-id').first()
            # order_by('-id')를 사용하여 가장 최근에 생성된 질문을 가져옵니다.
            print(f"Current question fetched: {question.question_text}")  # 디버깅용
            return {               
                'question_id': question.id,
                'text': question.question_text,
                'q_type': question.question_type,
                'choices': list(question.choices.values('id', 'choice_text')) if question.question_type != 'TEXT' else []
            }
        except Question.DoesNotExist:
            return None
# 

    async def poll_update_message(self, event):

        await self.send_poll_question()
        # await self.send(text_data=json.dumps(data, ensure_ascii=False))

    @database_sync_to_async
    def poll_result(self, question_id):
        from .models import Question, Choice, Answer
        try:
            question = Question.objects.get(id=question_id)
            if question.question_type in ['SINGLE', 'MULTIPLE']:
                results = list(question.choices.values('id', 'choice_text', 'votes_count'))
            else:  # TEXT 유형일 때
                results = list(Answer.objects.filter(question=question).values('answer_text'))
            return results
        except Question.DoesNotExist:
            return []