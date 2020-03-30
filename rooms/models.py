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
    room_type = models.CharField(max_length=10,choices=TYPES)
    invite_url = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rooms:room_detail',args=[self.slug])

    # def generate_invite_url(self):
    #     return base64.urlsafe_b64encode(uuid.uuid1().bytes.encode("base64").rstrip())[:25]

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.invite_url = self.generate_invite_url()
    #     elif not self.invite_url:
    #         self.invite_url = self.generate_invite_url()
    #     return super(Room,self).save(*args, **kwargs)


