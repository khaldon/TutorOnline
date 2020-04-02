from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.views.generic import ListView, DetailView
from .models import Room
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import RoomForm
from django.http import HttpResponseNotFound
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm
# Create your views here.

User = settings.AUTH_USER_MODEL

class RoomsView(ListView):
    model = Room
    queryset = Room.objects.all()
    paginate_by = 15
    template_name = 'rooms/rooms.html'
    context_object_name = 'rooms'


class RoomDetail(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room_detail'

@login_required
def join_room(request,room): 
    user = request.user
    join_to_room(user, room)
    return HttpResponse(room.students.count())

def join_to_room(user, room):
    room = get_object_or_404(Room,slug=room)
    room.students.add(user)
    return room.get_absolute_url()


def per_room(request, room):
    user = request.user
    if request.user.is_student:
        print("I'm student")
    elif request.user.is_teacher:
        print("I'm teacher")
        # assign_perm('password_check', user, room)
        assign_perm('pass_perm', user, room)
    else:
        print("error in permission")
    return HttpResponse("user")


    # if request.user.is_student:
    #     print("I'm student")
    # elif request.user.is_teacher:
    #     print("I'm teacher")
    #     # assign_perm('password_check', user, room)
    #     print(assign_perm('password_check', user, room))
    # else:
    #     print("error in permission")
    
    # return HttpResponse("room")
    
    # return render(request, 'rooms/check_per.html')
    
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
    
@login_required
def submit_invite(request,room):
    invite_url= request.GET['key']
    room = get_object_or_404(Room,slug=room)
    if room.invite_url != invite_url:
        return HttpResponseNotFound
    return room.get_absolute_url()

