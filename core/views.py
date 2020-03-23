from django.shortcuts import render,redirect
from users.models import user_type

# Create your views here.

def shome(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
        return render(request,'student_home.html')
    elif request.user.is_authenticated and user_type.objects.get(user=request.user).is_teacher:
        return redirect('thome')
    else:
        return redirect('users:login')
                      
def thome(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teacher:
        return render(request,'teacher_home.html')
    elif request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
        return redirect('shome')
    else:
        return redirect('users:login')