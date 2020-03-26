from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('s/',views.shome,name='student_home'),
    path('t/',views.thome,name='teacher_home'),

]
