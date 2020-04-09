import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
class Consumer(WebsocketConsumer):
    def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name
        self.name = self.scope['user'].username
        print("room_name {0}".format(self.room_name))
        print("room_group_name {0}".format(self.room_group_name))
        print("room {0}".format(self.name))
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.name+" Joined Chat "
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

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':self.name+" : "+message
            }
        )

    def chat_message(self,event):
        message=event['message']

        self.send(text_data=json.dumps({
            'message':message
        }))