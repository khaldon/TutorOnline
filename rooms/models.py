from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from users.models import Subject
import short_url

# Create your models here.

User = settings.AUTH_USER_MODEL

TYPES = [
    ('public','Public'),
    ('private','Private')
]

class Room(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500)
    students = models.ManyToManyField(User,related_name='room_students',blank=True)
    created = models.DateTimeField(default=timezone.now)
    subjects = models.ManyToManyField(Subject,related_name='room_subjects',blank=True)
    stream_time = models.TimeField()
    max_students_amount = models.PositiveIntegerField()
    room_type = models.CharField(choices=TYPES)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rooms:room',args=[self.slug])

    def short_url(self):
        _url = short_url.encode(self.get_absolute_url()+'join/')
        return _url
