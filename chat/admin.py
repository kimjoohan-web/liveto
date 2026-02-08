from django.contrib import admin

# Register your models here.
from .models import ChatRoom, Message # 모델 가져오기

admin.site.register(ChatRoom)
admin.site.register(Message)