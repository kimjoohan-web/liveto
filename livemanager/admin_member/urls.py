from django.urls import path

from . import views
app_name = 'admin_member'
urlpatterns = [
    path('', views.admin_list, name='admin_list'), 
    path('admin_list/', views.admin_list, name='admin_list'),
    path('admin_create/', views.admin_create, name='admin_create'),    
    path('admin_update/<int:admin_idx>/', views.admin_update, name='admin_update'),
    path('admin_detail/<int:admin_idx>/', views.admin_detail, name='admin_detail'),
    path('admin_delete/<int:admin_idx>/', views.admin_delete, name='admin_delete'),
  
]