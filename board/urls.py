from django.urls import path

from . import views
app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    path('board_create/', views.board_create, name='board_create'),
    path('<int:car_idx>/', views.board_detail, name='board_detail'),
    path('<int:car_idx>/board_update/', views.board_update, name='board_update'),
    path('<int:car_idx>/board_delete/', views.board_delete, name='board_delete'),

    # path('<str:room_name>/', views.room, name='room'),
    # path('<str:room_name>/messages/', views.MessageListView.as_view(), name='message_list'),
    
]