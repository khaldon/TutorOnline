from django import forms
from .models import Room
from users.models import Subject
# from django.http import Http404
class RoomForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),required=False)
    room_pass = forms.CharField(required=False)
    class Meta:
        model = Room
        fields = ('title','description','stream_time','max_students_amount','subjects','room_type','room_pass')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['stream_time'].widget.attrs.update({'autocomplete':'off'})   

class AuthRoomForm(forms.ModelForm):
    password2 = forms.CharField(max_length=150)
    class Meta:
        model = Room 
        fields = ('room_pass',)    
        exclude = ['room_pass']


class SearchStudentForm(forms.Form):
    student_query = forms.CharField(max_length=200)
    
