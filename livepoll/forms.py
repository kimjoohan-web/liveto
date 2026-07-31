# livepoll/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['live_stream', 'question_text', 'question_type', 'is_voting_now']
        widgets = {
            'live_stream': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '질문 내용을 입력하세요'}),
            'question_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_question_type'}),
            'is_voting_now': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_voting_now': '현재 투표 진행 여부',
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control choice-input', 'placeholder': '보기 내용을 입력하세요'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 빈 칸이어도 Validation을 통과할 수 있도록 False 처리
        self.fields['choice_text'].required = False

    
# Question 하나에 속한 Choice들을 한 번에 관리하는 폼셋 생성 (기본 2개 생성)
ChoiceFormSet = inlineformset_factory(
    Question, 
    Choice, 
    form=ChoiceForm, 
    extra=2,          # 처음에 기본으로 보여줄 보기 입력창 개수
    can_delete=True  # 생성 페이지이므로 삭제 체크박스 포함
)

