from django.urls import path
from .views import RoomsView,join_room,create_room

app_name = 'rooms'

urlpatterns = [
    path('rooms/',RoomsView.as_view(),name='rooms'),
    path('rooms/<room>/',join_room,name='join_room'),
    path('rooms/create_room/',create_room,name='create_room'),
]