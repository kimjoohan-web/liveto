from django.urls import path

from . import views
app_name = 'livemanager'
urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'), 
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('event_list/', views.event_list, name='event_list'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('member_list/', views.member_list, name='member_list'),
    path('member_detail/<int:member_id>/', views.member_detail, name='member_detail'),
    path('board_list/', views.board_list, name='board_list'),
    path('board_detail/<int:post_id>/', views.board_detail, name='board_detail'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('member_pending/', views.member_pending, name='member_pending'),
    path('member_search/', views.member_search, name='member_search'),
    path('event_create/', views.event_create, name='event_create'),
    path('event_category/', views.event_category, name='event_category'),
    path('inquiry_list/', views.inquiry_list, name='inquiry_list'),
    path('comment_list/', views.comment_list, name='comment_list'),

    # path('member/', views.index, name='index'), 
    path('member_input/', views.member_input, name='member_input'),
    path('mem_login/', views.mem_login, name='mem_login'),
    path('member_modify/<str:mem_idx>/', views.member_modify, name='member_modify'),
    path('member_delete/<str:mem_idx>/', views.member_delete, name='member_delete'),
    path('member_excel_download/', views.member_excel_download, name='member_excel_download'),
    path('member_excel_upload/', views.member_excel_upload, name='member_excel_upload'),    
    path('member_bulk_delete/', views.member_bulk_delete, name='member_bulk_delete'),
    path('member_logout/', views.member_logout, name='member_logout'),
]