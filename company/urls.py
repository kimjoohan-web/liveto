from django.urls import path

from . import views
app_name = 'company'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('business/', views.business, name='business'),
    path('clients/', views.clients, name='clients'),
    path('works/', views.works, name='works'),
    path('location/', views.location, name='location'),
]