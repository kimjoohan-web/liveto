from django.urls import path

from . import views
app_name = 'livemanager'
urlpatterns = [
    path('', views.index, name='index'), 
    path('member/', views.index, name='index'), 
    path('member_input/', views.member_input, name='member_input'),
    path('mem_login/', views.mem_login, name='mem_login'),
    path('member_modify/<str:mem_idx>/', views.member_modify, name='member_modify'),
    path('member_delete/<str:mem_idx>/', views.member_delete, name='member_delete'),
    path('member_excel_download/', views.member_excel_download, name='member_excel_download'),
    path('member_excel_upload/', views.member_excel_upload, name='member_excel_upload'),    
    path('member_bulk_delete/', views.member_bulk_delete, name='member_bulk_delete'),
    path('member_logout/', views.member_logout, name='member_logout'),
]