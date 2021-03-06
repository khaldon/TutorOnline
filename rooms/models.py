from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from users.models import Subject
import short_url
import uuid
import base64

# Create your models here.

User = settings.AUTH_USER_MODEL

class Room(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500)
    teacher = models.ManyToManyField(User,related_name='teacher_rooms')
    students = models.ManyToManyField(User,related_name='room_students',blank=True)
    created = models.DateTimeField(default=timezone.now)
    subjects = models.ManyToManyField(Subject,related_name='room_subjects',blank=True)
    stream_time = models.TimeField()
    max_students_amount = models.PositiveIntegerField()
    invite_url = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    room_pass = models.CharField(max_length=150, default='')
    banned_users = models.ManyToManyField(User, related_name='forbidden_groups',blank=True)


    class Meta:
        ordering = ('-created',)
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('pass_perm', 'Pass permission'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rooms:room_detail',args=[str(self.invite_url)])