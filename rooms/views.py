from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.views.generic import ListView, DetailView
from .models import Room
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import RoomForm, AuthRoomForm,SearchStudentForm
from django.http import HttpResponseNotFound
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm
from users.models import CustomUser
from django.contrib import messages
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .documents import RoomDocument

# Create your views here.

User = settings.AUTH_USER_MODEL

class RoomsView(ListView):
    model = Room
    queryset = Room.objects.all()
    paginate_by = 15
    template_name = 'rooms/rooms.html'
    context_object_name = 'rooms'
def room_detail(request,room_name):
    print("hello world")
    if request.user.is_anonymous:
        print("hello annonymous")
    else:
        print("no ")
    room_name = get_object_or_404(Room,invite_url=room_name)
    return render(request,'rooms/room_detil.html',{'room_name':room_name,})


@login_required
def join_room(request,uuid):
    room = get_object_or_404(Room,invite_url=uuid)
    user = request.user
    room.students.add(user)
    return HttpResponseRedirect(Room.get_absolute_url(room))

def leave_room(request,uuid):
    room = get_object_or_404(Room,invite_url=uuid)
    user = request.user
    room.students.remove(user)
    return redirect('rooms:rooms')

def banned_students(request):
    teacher = get_object_or_404(CustomUser,username=request.user.username)
    teacher = teacher.teacher_rooms.all()
    return render(request, 'rooms/banned_students.html', {'teacher_room':teacher})

def ban_student(request, uuid, user_id):
    room = get_object_or_404(Room, invite_url=uuid)
    student = get_object_or_404(CustomUser, id=user_id)
    if student in room.students.all():
        room.banned_users.add(student)
        room.students.remove(student)
        return redirect('rooms:student_banned')
    else:
        room.banned_users.remove(student)
        room.students.add(student)
        return redirect('rooms:student_banned')

def auth_join(request, room, uuid):
    room = get_object_or_404(Room, invite_url=uuid)
    if request.user in room.teacher.all():
        return HttpResponseRedirect(Room.get_absolute_url(room))
    join_key = f"joined_{room.invite_url}"
    if request.session.get(join_key, False):
        join_room(request,uuid)
        return HttpResponseRedirect(Room.get_absolute_url(room))
    else:
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
                    user = CustomUser.objects.get(username=user)
                    try:
                        room = get_object_or_404(Room, invite_url=uuid)
                    except ValueError:
                        raise Http404
                    assign_perm('pass_perm',user, room)
                    if user.has_perm('pass_perm', room):
                        request.session[join_key] = True
                        join_room(request,uuid)
                        return HttpResponseRedirect(Room.get_absolute_url(room))
                    else:
                        return HttpResponse('Problem issues')
        else:
            form_auth = AuthRoomForm()
        return render(request,'rooms/auth_join.html', {'form_auth':form_auth, 'uuid':uuid})


def per_room(request, room):
    user = request.user.username
    user = CustomUser.objects.get(username=user)

    if request.user.is_student:
        print("I'm student")
    elif request.user.is_teacher:        # assign_perm('password_check', user, room)
        assign_perm('pass_perm', user, room)
    else:
        print("error in permission")
    return HttpResponse("user")

class TeacherCreatedRooms(LoginRequiredMixin,ListView):
    model = Room
    paginate_by = 20
    template_name = 'rooms/teacher_created_rooms.html'
    context_object_name = 'teacher_rooms'

    def get_queryset(self,**kwargs):
        user = get_object_or_404(CustomUser,username=self.request.user.username)
        return user.teacher_rooms.all()

@login_required
def create_room(request):
    room_form = RoomForm()
    if request.method == 'POST':
        room_form = RoomForm(request.POST,request.FILES)
        if room_form.is_valid():
            new_room = room_form.save()
            new_room.teacher.add(request.user)
            return redirect(new_room.get_absolute_url())
    else:
        room_form = RoomForm()
    return render(request,'rooms/create_room.html',{'room_form':room_form})

def show_chat_page(request,room_name):
    room = get_object_or_404(Room,invite_url=room_name)
    return render(request,"rooms/room_detail.html",{'room_name':room_name,'room':room})

def room_search(request):
    form = SearchStudentForm(request.GET)
    query = None 
    results = None 
    if form.is_valid():
        query = form.cleaned_data['student_query']
        results = RoomDocument.search().filter("term",title=query)
        results = results.to_queryset()
    return render(request,'rooms/student_search.html', {'form':form,'query':query,'results':results})

