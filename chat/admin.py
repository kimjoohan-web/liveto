from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from .models import ChatRoom, Message # 모델 가져오기
admin.site.register(ChatRoom,Message)




