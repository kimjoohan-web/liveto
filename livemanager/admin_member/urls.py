from django.urls import path

from . import views
app_name = 'admin_member'
urlpatterns = [
    path('', views.admin_list, name='admin_list'), 
    path('admin_list/', views.admin_list, name='admin_list'),
    path('admin_create/', views.admin_create, name='admin_create'),    
    path('admin_update/<int:admin_idx>/', views.admin_update, name='admin_update'),
  
]