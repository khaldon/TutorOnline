from django.shortcuts import render,redirect,get_object_or_404
from .models import Course
from .forms import CourseForm
from users.decorators import teacher_required
from django.contrib.auth.decorators import login_required
from .decorators import course_tutor

# Create your views here.

@login_required
@teacher_required
def create_course(request):
    course_form = CourseForm()
    if request.method == 'POST':
        course_form = CourseForm(request.POST,request.FILES)
        if course_form.is_valid():
            new_course = course_form.save()
            new_course.tutor.add(request.user)
            return redirect(new_course.get_absolute_url())
    else:
        course_form = CourseForm()
    return render(request,'courses/create_course.html',{'course_form':course_form})

@login_required
@course_tutor
def edit_course(request,course):
    course = get_object_or_404(Course,slug=course)
    if request.method == 'POST':
        course_form = CourseForm(instance=course,data=request.POST,files=request.FILES)
        if course_form.is_valid():
            course_form.save()
            return redirect(course.get_absolute_url())
        else:
            course_form = CourseForm(instance=course)
    else:
        course_form = CourseForm(instance=course)
    return render(request,'courses/edit_course.html',{'course_form':course_form})