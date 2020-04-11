from django.urls import path
from .views import (RoomsView,create_room,RoomDetail,
                    per_room,auth_join,TeacherCreatedRooms,
                    join_room,leave_room,show_chat_page,
                    banned_students, ban_student)

app_name = 'rooms'

urlpatterns = [
    path('rooms/check_pre/<room>',per_room, name='check_pre'),
    path('rooms/forms/<room>/<uuid>/', auth_join, name='auth_join' ),
    path('rooms/<str:room_name>/',show_chat_page, name='room_detail'),
    path('rooms/',RoomsView.as_view(),name='rooms'),
    path('create_room/',create_room,name='create_room'),
    path('<username>/rooms/',TeacherCreatedRooms.as_view(),name='teacher_created_rooms'),
    path('rooms/<uuid>/join/',join_room,name='join_room'),
    path('rooms/<uuid>/leave/',leave_room,name='leave_room'),
    path('rooms/banned_student/<uuid>/', banned_students,name='banned_student'),
    path('rooms/ban_student/<uuid>/<user_id>/',ban_student, name='ban_student')
]