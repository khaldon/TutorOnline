from django.shortcuts import render,redirect
from django.urls import  reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate
from .models import User
from django.views.generic import CreateView,TemplateView
from .forms import StudentSignUpForm,TeacherSignUpForm
from django.contrib.auth import login as auth_login

# Create your views here.

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('core:shome')

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request,user,backend='django.contrib.auth.backends.ModelBacked')
        return redirect('core:thome')
        