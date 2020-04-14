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
    discount_price = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = course_slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_add_to_cart_url(self):
        return reverse("courses:add-to-cart",kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("courses:remove_from_cart",kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('courses:course',args=[self.slug])

    def __str__(self):
        return self.title

class OrderCourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def get_total_discount_course_price(self):
        return self.course.discount_price

    def get_total_course_price(self):
        return self.course.price

    def get_final_price(self):
        if self.course.discount_price:
            return self.get_total_discount_course_price()
        return self.get_total_course_price()

    def get_amount_saved(self):
        return self.get_total_course_price() - self.get_total_discount_course_price()

    def __str__(self):
        return self.course.title

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    courses = models.ManyToManyField(OrderCourse)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)

    def get_total(self):
        total = 0
        for order_course in self.courses.all():
            total += order_course.get_final_price()
        return total

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class PaymentInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,default=False)
    last_name = models.CharField(max_length=100,default=False)

    def __str__(self):
        return '{} {} {}'.format(self.user.username,self.first_name,self.last_name)

class Review(models.Model):
    course = models.ForeignKey(Course,related_name='reviews',on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='posted_comments', on_delete=models.CASCADE)
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.reviewer + ' ' + self.body

course_slugify = UniqueSlugify(
                    to_lower=True,
                    max_length=80,
                    separator='_',
                    capitalize=False
                )