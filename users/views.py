from django.shortcuts import render,redirect
from .forms import UserCreation
from django.urls import  reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate,login
from .models import user_type, User

# Create your views here.

def signup(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        st = request.POST.get('student')
        te = request.POST.get('teacher')
        user = User.objects.create_user(
            email=email,
        )
        user.set_password(password)
        user.save()
        usert = None
        if st:
            usert = user_type(user=user,is_student=True)
        elif te:
            usert = user_type(user=user,is_teach=True)
        usert.save()
        return redirect('home')
    return render(request, 'users/registration/signup.html')

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