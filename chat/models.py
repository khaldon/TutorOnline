import uuid
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()

class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(User, related_name='teacher_room', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='student_room', on_delete=models.CASCADE)


class Message(models.Model):
    teacher = models.ForeignKey(User, related_name='teahcer_messages', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='student_messages', on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.DO_NOTHING)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message + " " + str(self.timestamp)