from django.db import models
from django.conf import settings
from django.utils import timezone
from languages.fields import LanguageField
from slugify import UniqueSlugify
from django.urls import reverse

# Create your models here.

User = settings.AUTH_USER_MODEL

class CourseCategories(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class SectionVideos(models.Model):
    video = models.FileField(upload_to='courses/section_videos')

class CourseSections(models.Model):
    title = models.CharField(max_length=50)
    video = models.ForeignKey(SectionVideos,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    section = models.ForeignKey(CourseSections,related_name='course_sections',on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/course_images',blank=True,null=True)
    cover = models.ImageField(upload_to='courses/course_covers',blank=True,null=True)
    tutor = models.ForeignKey(User,related_name='tutor_courses',on_delete=models.CASCADE)
    students = models.ForeignKey(User,related_name='course_students',blank=True,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(CourseCategories,on_delete=models.CASCADE)
    certificate = models.ImageField(upload_to='courses/course_certificates',blank=True,null=True)
    languages = LanguageField(blank=True)
    rank_score = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = course_slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:course',args=[self.slug])

class Review(models.Model):
    course = models.ForeignKey(Course,related_name='reviews',on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='posted_comments', on_delete=models.CASCADE)
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

course_slugify = UniqueSlugify(
                    to_lower=True,
                    max_length=80,
                    separator='_',
                    capitalize=False
                )