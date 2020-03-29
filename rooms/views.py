from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.views.generic import ListView
from .models import Room
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import RoomForm

# Create your views here.

User = settings.AUTH_USER_MODEL

class RoomsView(ListView):
    model = Room
    queryset = Room.objects.all()
    paginate_by = 15
    template_name = 'rooms/rooms.html'
    context_object_name = 'rooms'

@login_required
def join_room(request,room):
    room = get_object_or_404(Room,slug=room)
    user = request.user
    room.students.add(user)
    return HttpResponse(room.students.count())

@login_required
def create_room(request):
    room_form = RoomForm()
    if request.method == 'POST':
        room_form = RoomForm(request.POST,request.FILES)
        if room_form.is_valid():
            new_room = room_form.save()
            return redirect(new_room.get_absolute_url())
    else:
        room_form = RoomForm()
    return render(request,'rooms/create_room.html',{'room_form':room_form})
    