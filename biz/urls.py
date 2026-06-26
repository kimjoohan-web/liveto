from django.urls import path

from . import views
app_name = 'biz'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('webcasting', views.webcasting, name='webcasting'),
    path('elearning', views.elearning, name='elearning'),
    path('relay', views.relay, name='relay'),
    path('station', views.station, name='station'),
    path('video', views.video, name='video'),
    path('homepage', views.homepage, name='homepage'),
    path('eseminar', views.eseminar, name='eseminar'),
    

    # path('<str:room_name>/', views.room, name='room'),
    # path('<str:room_name>/messages/', views.MessageListView.as_view(), name='message_list'),
    
]