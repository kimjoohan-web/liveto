from django.urls import path

from . import views
app_name = 'works'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),  
    path('<int:car_idx>/', views.detail, name='detail'),
]