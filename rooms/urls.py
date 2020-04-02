from django.urls import path
from .views import RoomsView,create_room, RoomDetail, per_room, auth_join

app_name = 'rooms'


urlpatterns = [
    path('rooms/check_pre/<room>',per_room, name='check_pre'),
    path('rooms/forms/<room>/<slug:slug>', auth_join, name='auth_join' ),

    path('rooms/<slug:slug>/', RoomDetail.as_view(), name='room_detail'),
    path('rooms/',RoomsView.as_view(),name='rooms'),
    path('create_room/',create_room,name='create_room'),
    # path('rooms/<room>/',join_room,name='join_room'),

    # path('rooms/<room>/invite?key=<invite_url>/',join_to_room,name='join_to_room'),
]