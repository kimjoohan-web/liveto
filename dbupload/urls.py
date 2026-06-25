from django.urls import path

from . import views
app_name = 'dbupload'
urlpatterns = [
    path('', views.index, name='index'),  
    path('db_excel_upload/', views.db_excel_upload, name='db_excel_upload'),

    # path('<str:room_name>/', views.room, name='room'),
    # path('<str:room_name>/messages/', views.MessageListView.as_view(), name='message_list'),
    
]