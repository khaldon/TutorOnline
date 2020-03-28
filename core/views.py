from django.shortcuts import render,redirect


# Create your views here.

def home(request):
    if request.user.is_authenticated and request.user.is_student:
        return render(request,'student_home.html')
    if request.user.is_authenticated and request.user.is_teacher:
        return render(request,'teacher_home.html')
    return render(request,'home.html')
        
def dashboard(request):
    return render(request, 'base.html')

# def shome(request):
#     if request.user.is_authenticated and request.user.is_student:
#         return render(request,'student_home.html')
#     elif request.user.is_authenticated and request.user.is_teacher:
#         return redirect('core:dashboard')
#     else:
#         return redirect('users:login')
                      
# def thome(request):
#     if request.user.is_authenticated and request.user.is_teacher:
#         return render(request,'teacher_home.html')
#     elif request.user.is_authenticated and request.user.is_student:
#         return redirect('core:dashboard')
#     else:
#         return redirect('users:login')