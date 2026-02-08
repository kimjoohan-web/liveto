from django.contrib import admin
from django.utils.html import format_html


# Register your models here.
from .models import ChatRoom, Message # 모델 가져오기
@admin.register(ChatRoom)
@admin.register(Message)


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # 관리자 페이지에 표시할 필드


class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_room', 'sender', 'content', 'timestamp')  # 관리자 페이지에 표시할 필드
    search_fields   = ('sender', 'content')  # 검색 필드 설정   

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)  