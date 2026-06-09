from django.urls import path

from . import views
app_name = 'livemanager'
urlpatterns = [
    path('', views.index, name='index'), 
    path('member/', views.index, name='index'), 
    path('member_input/', views.member_input, name='member_input'),
    path('mem_login/', views.mem_login, name='mem_login'),
    
]