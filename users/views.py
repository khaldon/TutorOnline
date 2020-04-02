from django.shortcuts import render,redirect
from django.urls import  reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate
from .models import CustomUser
from django.views.generic import CreateView,TemplateView
from .forms import StudentSignUpForm,TeacherSignUpForm, CustomUserCreationForm,UserEditForm,StudentProfileForm,TeacherProfileForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.conf import settings

# Create your views here.

User = settings.AUTH_USER_MODEL

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('core:dashboard')

class TeacherSignUpView(CreateView):
    model = CustomUserCreationForm
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request,user,backend='django.contrib.auth.backends.ModelBacked')
        return redirect('core:dashboard')
    
@login_required
def profile(request):
    if request.method == 'POST':
        if request.user.is_student:
            user_form = UserEditForm(request.POST, instance=request.user)
            profile_form = StudentProfileForm(request.POST,request.FILES, instance=request.user.profile)
        else:
            user_form = UserEditForm(request.POST, instance=request.user)
            profile_form = TeacherProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated')
        else:
            messages.error(request, 'Please correct that errors in your profile form.')
    else:
        user_form = UserEditForm(instance=request.user)
        if request.user.is_student:
            profile_form = StudentProfileForm(instance=request.user.profile)
        else:
            profile_form = TeacherProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
        'user_form':user_form,
        'profile_form':profile_form
    })

def delete_user(request, username):
    u = CustomUser.objects.get(username=username)
    u.delete()
    return redirect('core:home')
    