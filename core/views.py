from django.shortcuts import render,redirect

# Create your views here.



def home(request):
    return render(request, 'home.html')

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