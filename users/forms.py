from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,Student,StudentInterests,TeacherMajors
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class TeacherSignUpForm(UserCreationForm):
    email = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    
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
    email = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    studentinterests = forms.ModelMultipleChoiceField(
        queryset=StudentInterests.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','studentinterests',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.studentinterests = self.cleaned_data["studentinterests"]
        if commit:
            user.save()
        return user

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

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))