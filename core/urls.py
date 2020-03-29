from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('room/', views.room, name='room')
]
