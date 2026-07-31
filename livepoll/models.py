from django.db import models
from django.conf import settings

# import 윗단계
# 절대경로 



# Create your models here.

class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    stream_url = models.URLField() # video.js에서 사용할 HLS(.m3u8) 주소
    is_live = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPE_CHOICES = [
        ('SINGLE', '단일 선택'),
        ('MULTIPLE', '다중 선택'),
        ('TEXT', '주관식'),
    ]
    # 어떤 라이브 방송의 질문인지 연결
    live_stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    # 관리자가 '이 문제를 실시간 송출' 중인지 여부
    is_voting_now = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

# Choice와 Answer 모델은 이전 설계를 그대로 유지합니다.


class Choice(models.Model):
    # 객관식 질문(SINGLE, MULTIPLE)일 때만 데이터가 생성됩니다.
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=250)
    votes_count = models.IntegerField(default=0) # (선택사항) 빠른 통계를 위한 카운트 필드

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    # 투표를 제출한 유저 (비회원 투표 허용 시 null=True, blank=True)
    # user 필드는 member.event_member 테이블과 연결되어야 합니다.

    user = models.ForeignKey(
        'member.event_member',  # event_member 모델의 mem_idx 필드와 연결
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # 1. 객관식 답변인 경우 (다중 선택을 고려하여 ManyToMany로 연결)
    # 단일 선택이어도 이 필드에 1개의 객체만 담으면 되므로 일관성 있게 관리 가능합니다.
    selected_choices = models.ManyToManyField(Choice, blank=True)
    
    # 2. 주관식 답변인 경우 (TEXT 유형일 때 사용)
    answer_text = models.TextField(null=True, blank=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user if self.user else '비회원'}의 {self.question.id}번 질문 답변"




