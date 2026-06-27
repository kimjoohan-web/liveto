from django.urls import path

from . import views
app_name = 'customer'
urlpatterns = [ 
    path('', views.index, name='index'),   
    path('index/', views.index, name='index'),
    path('<int:car_idx>/', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy')
    
    
]