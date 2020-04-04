from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.views.generic import ListView, DetailView
from .models import Room, TYPES
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import RoomForm, AuthRoomForm
from django.http import HttpResponseNotFound
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm
from users.models import CustomUser
from django.contrib import messages
from users.models import CustomUser
from django.urls import reverse
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
    slug_field = 'invite_url'
    slug_url_kwarg = 'url'

def auth_join(request, room, uuid):
    try:
        room_type = getattr(Room.objects.get(invite_url=uuid), 'room_type')
    except ValueError:
        raise Http404
    if room_type == 'private':
        if request.method == 'POST':
            user = request.user.username    
            form_auth = AuthRoomForm(request.POST)
            if form_auth.is_valid():
                try:
                    room_pass = getattr(Room.objects.get(invite_url=uuid), 'room_pass')
                except ValueError: 
                    raise Http404
                password2 = form_auth.cleaned_data.get('password2')
                if room_pass != password2:
                    messages.error(request, 'Doesn\'t match')
                    return HttpResponseRedirect(request.get_full_path())
                else:
                    # messages.success(request, 'match')
                    user = CustomUser.objects.get(username=user)
                    try:
                        room = get_object_or_404(Room, invite_url=uuid)
                    except ValueError:
                        raise Http404

                    assign_perm('pass_perm',user, room)
                    if user.has_perm('pass_perm', room):
                        return HttpResponseRedirect(Room.get_absolute_url(room))
                    else:
                        return HttpResponse('Problem issues')
        else:
            form_auth = AuthRoomForm()
        return render(request,'rooms/auth_join.html', {'form_auth':form_auth})
    else:
        return HttpResponse('this work on private room only')

def per_room(request, room):
    user = request.user.username
    print("user one {0}".format(user))
    user = CustomUser.objects.get(username=user)
    print("user two {0}".format(user))

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

