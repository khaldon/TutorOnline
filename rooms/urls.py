from django.urls import path
from .views import RoomsView,join_room,create_room

app_name = 'rooms'

urlpatterns = [
    path('',RoomsView.as_view(),name='rooms'),
    path('create_room/',create_room,name='create_room'),
    path('<rooms>/',join_room,name='join_room'),
]   