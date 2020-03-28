from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,AbstractUser
from django.utils import timezone
from django_countries.fields import CountryField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

User = settings.AUTH_USER_MODEL

# Create your models here.

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female')
]

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class StudentInterests(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser): 
    email =  models.EmailField(_('email_address'), unique=True, name='email')
    username =  models.CharField(_('username'), unique=True, max_length=128)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

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

class Profile(models.Model):
    # common fields
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name='birth_date',blank=True,null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    slug = models.SlugField(max_length=255,unique=True,null=True,blank=True)
    country = CountryField()
    city = models.CharField(max_length=255,null=True,blank=True)
    bio = models.CharField(max_length=300)
    image = models.ImageField(verbose_name='userimages',upload_to='user_images',null=True,blank=True)
    # student fields
    interests = models.ManyToManyField(StudentInterests,blank=True)
    # teacher fields
    course = models.ManyToManyField(Course,blank=True)
    rating = models.FloatField(default=0)
    students = models.ManyToManyField(User,related_name='students')
    subjects = models.ManyToManyField(Subject)

    def get_student(self):
        return self.user.is_student == True

    def get_teacher(self):
        return self.user.is_teacher == True

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
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()