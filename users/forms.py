from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,Student,StudentInterests

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=StudentInterests.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email',)



class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('email', 'username' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None 

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)
