from django import forms
from .models import Room
from users.models import Subject

class RoomForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),required=False)

    class Meta:
        model = Room
        fields = ('title','description','stream_time','max_students_amount','subjects','room_type')
        widgets = {'room_type':forms.RadioSelect}