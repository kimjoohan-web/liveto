from django.urls import path

from . import views
app_name = 'event_board'
urlpatterns = [
    path('', views.event_list, name='event_list'), 
    path('event_list/', views.event_list, name='event_list'),
    path('event_create/', views.event_create, name='event_create'),    
    path('event_update/<int:event_idx>/', views.event_update, name='event_update'),
    path('event_detail/<int:event_idx>/', views.event_detail, name='event_detail'),    
    path('event_delete/<int:event_idx>/', views.event_delete, name='event_delete'),    
    path('event_bulk_delete/', views.event_bulk_delete, name='event_bulk_delete'),
]