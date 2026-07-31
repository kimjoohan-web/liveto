from django.urls import path

from . import views
app_name = 'livepoll'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_poll/', views.create_poll, name='create_poll'),    
    path('modify_poll/<int:question_id>/', views.modify_poll, name='modify_poll'),
    path('delete_poll/<int:question_id>/', views.delete_poll, name='delete_poll'),
    path('livepoll_list/', views.livepoll_list, name='livepoll_list'),
    path('create_livestream/', views.create_livestream, name='create_livestream'),
    path('livestream_list/', views.livestream_list, name='livestream_list'),
    path('stream_view/<int:stream_id>/', views.stream_view, name='stream_view'),
    path('modify/<int:stream_id>/', views.modify_livestream, name='modify_livestream'),
    path('go_poll/<int:question_id>/', views.go_poll, name='go_poll'),
    path('submit_vote/<int:question_id>/', views.submit_vote, name='submit_vote'),
    
    
    
]