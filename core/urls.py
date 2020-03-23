from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('s/',views.shome,name='student_home'),
    path('t/',views.thome,name='teacher_home'),
]
