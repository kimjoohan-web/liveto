from django.urls import path

from . import views
app_name = 'member'
urlpatterns = [
    # path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('member_input/', views.member_input, name='member_input'),
    path('mem_login/', views.mem_login, name='mem_login'),
    path('member_modify/<str:mem_idx>/', views.member_modify, name='member_modify'),
    path('member_delete/<str:mem_idx>/', views.member_delete, name='member_delete'),
    path('member_logout/', views.member_logout, name='member_logout'),
    
    

]