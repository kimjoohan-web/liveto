from django.urls import path

from . import views
app_name = 'livemanager'
urlpatterns = [
    path('', views.index, name='index'), 
    path('member/', views.index, name='index'), 
    
]