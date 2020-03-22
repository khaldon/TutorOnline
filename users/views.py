from django.shortcuts import render
from .forms import UserCreation
from django.urls import  reverse_lazy
from django.views import generic


# Create your views here.

class Signup(generic.CreateView):
    form_class = UserCreation
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users:login')