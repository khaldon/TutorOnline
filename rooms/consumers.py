import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class Consumer(WebsocketConsumer):
    def connect(self):
        self.url=self.scope['url_route']['kwargs']['url']
        self.room_group_name='chat_%s' % self.url
        self.user = self.request.user

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.user+" Joined Chat"
            }
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.user+" Left Chat"
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':self.user+" : "+message
            }
        )

    def chat_message(self,event):
        message=event['message']

        self.send(text_data=json.dumps({
            'message':message
        }))