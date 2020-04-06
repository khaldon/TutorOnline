from django.urls import re_path

from rooms.consumer import Consumer

websocket_urlpatterns=[
    re_path(r'ws/chat/(?P<room_name>\w+)/$',Consumer)
]