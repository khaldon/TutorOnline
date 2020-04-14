from django.contrib import admin
from .models import Course,CourseSections,CourseCategories

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseSections)
admin.site.register(CourseCategories)