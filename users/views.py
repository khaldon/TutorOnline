from django.shortcuts import render,redirect
from django.urls import  reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate,login
from .models import User
from django.views.generic import CreateView,TemplateView
from .forms import StudentSignUpForm,TeacherSignUpForm

# Create your views here.

class SignUpView(TemplateView):
    template_name = 'users/registration/signup.html'

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'users/registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:shome')

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'users/registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:thome')

def login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            type_obj = user_type.objects.get(user=user)
            if user.is_authenticated and type_obj.is_student:
                return redirect('') #Go to student home
            elif user.is_authenticated and type_obj.is_teach:
                return redirect('') #Go to teacher home
        else:
            # Invalid email or password. Handle as you wish
            return redirect('home')

    return render(request, 'users/registration/login.html')