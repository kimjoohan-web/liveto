from django.urls import path

from . import views
app_name = 'user_member'
urlpatterns = [
    path('', views.user_list, name='user_list'), 
    path('user_list/', views.user_list, name='user_list'),
    path('user_create/', views.user_create, name='user_create'),    
    path('user_update/<int:user_idx>/', views.user_update, name='user_update'),
    path('user_detail/<int:user_idx>/', views.user_detail, name='user_detail'),
    path('user_excel_create/', views.user_excel_create, name='user_excel_create'),
    path('user_delete/<int:user_idx>/', views.user_delete, name='user_delete'),
]