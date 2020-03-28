from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,StudentInterests,Profile,Subject,Course
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.conf import settings
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.widgets import ClearableFileInput

User = settings.AUTH_USER_MODEL

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'users/custom_clear_file_input.html'


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})
        self.fields['username'].widget.attrs.update({'placeholder':'username'})
        self.fields['email'].widget.attrs.update({'placeholder':'email'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})
        self.fields['username'].widget.attrs.update({'placeholder':'username'})
        self.fields['email'].widget.attrs.update({'placeholder':'email'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','email')

class TeacherProfileForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),required=False)
    course = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('birth_date','gender','country','city','bio','image','course','subjects')
        widgets = {
            'image':CustomClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].help_text = 'Pick your country from the list.'
        self.fields['city'].help_text = 'Provide your city.'
        self.fields['bio'].help_text = 'Tell people about your teacher career and everything related to that.'        
        self.fields['birth_date'].widget.attrs.update({'autocomplete':'off'})   

    

class StudentProfileForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset=StudentInterests.objects.all(),required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('birth_date','gender','country','city','bio','image','interests')
        widgets = {
            'image':CustomClearableFileInput(),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].help_text = 'Pick your country from the list.'
        self.fields['city'].help_text = 'Provide your city.'
        self.fields['bio'].help_text = 'Tell people what you want to archive here.'        
        self.fields['birth_date'].widget.attrs.update({'autocomplete':'off'})   

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None 
        

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))