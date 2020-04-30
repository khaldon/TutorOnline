from django.contrib import admin
from .models import Course,CourseSections,CourseCategories,SectionVideos, Wishlist

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseSections)
admin.site.register(CourseCategories)
admin.site.register(SectionVideos)
admin.site.register(Wishlist)