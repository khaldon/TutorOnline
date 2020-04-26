import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.http import HttpResponseRedirect
from users.models import CustomUser
from django.shortcuts import get_object_or_404
class Consumer(WebsocketConsumer):
    def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name
        self.name = self.scope['user'].username
        user = get_object_or_404(CustomUser,username=self.name)

        if self.scope['user'].is_anonymous:
            self.send({'close':True})
        else:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            if user.is_teacher:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type":"chat_message",
                        "message":" Joined Chat ",
                        'teacher':True,
                        'user':self.name
                    }
                )
            else:
                  async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type":"chat_message",
                        "message":" Joined Chat ",
                        'teacher':False,
                        'user':self.name
                    }
                )

            self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.name+" Left Chat"
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        user = get_object_or_404(CustomUser,username=self.name)
        if user.is_teacher:

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message':message,
                    'teacher':True,
                    'user':self.name
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message':message,
                    'teacher':False,
                    'user':self.name

                }
            )



    def chat_message(self,event):
        message=event['message'] 
        teacher = event['teacher']
        user = event['user']
        self.send(text_data=json.dumps({
            'message':message,
            'teacher':teacher,
            'user':user
        }))