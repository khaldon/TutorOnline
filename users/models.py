from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female')
]

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

class user_type(models.Model):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.is_student == True:
            return User.get_email(self.user) + " - is_student"
        else:
            return User.get_email(self.user) + " - is_teacher"

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name='student_birth_date',blank=True,null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    slug = models.SlugField(max_length=255,unique=True,null=True,blank=True)
    country = CountryField()
    city = models.CharField(max_length=255,null=True,blank=True)
    bio = models.CharField(max_length=300)

class StudentInterests(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='student_image',upload_to='student_images',null=True,blank=True)
    interests = models.ManyToManyField(StudentInterests,blank=True)

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/default_picture.png'
        if self.image:
            return self.image.url
        else:
            return default_picture

    def __str__(self):
        return self.user.email

class University(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    university = models.ForeignKey(University,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.title

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class TeacherProfile(models.Model):
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='teacher_image',upload_to='teacher_images',null=True,blank=True)
    course = models.ManyToManyField(Course,blank=True)
    rating = models.FloatField(default=0)
    students = models.ManyToManyField(User,related_name='students')
    subjects = models.ManyToManyField(Subject)

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/default_picture.png'
        if self.image:
            return self.image.url
        else:
            return default_picture

    def __str__(self):
        return self.user.email
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# @receiver(post_save, sender=User)
# def create_student_profile(sender, instance, created, **kwargs):
#     if created:
#         StudentProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def create_teacher_profile(sender, instance, created, **kwargs):
#     if created:
#         TeacherProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_student_profile(sender, instance, **kwargs):
#     instance.studentprofile.save()

# @receiver(post_save, sender=User)
# def save_teacher_profile(sender, instance, **kwargs):
#     instance.teacherprofile.save()
