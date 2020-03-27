from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,StudentInterests,TeacherMajors,Profile
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.conf import settings
from bootstrap_datepicker_plus import DatePickerInput

User = settings.AUTH_USER_MODEL

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
    studentinterests = forms.ModelMultipleChoiceField(
        queryset=StudentInterests.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.studentinterests = self.cleaned_data["studentinterests"]
        if commit:
            user.save()
        return user

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date','gender','country','city','bio','image','course','subjects')
        widgets = {
            'birth_date':DatePickerInput(format='%m/%d/%Y')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].help_text = 'Pick your birth date.'
        self.fields['country'].help_text = 'Pick your country from the list.'
        self.fields['city'].help_text = 'Provide your city.'
        self.fields['bio'].help_text = 'Tell people about your teacher career and everything related to that.'        
        self.fields['subjects'].help_text = 'Provide your subjects.'        

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date','gender','country','city','bio','image','interests')
        widgets = {
            'birth_date':DatePickerInput(format='%m/%d/%Y')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].help_text = 'Pick your birth date.'
        self.fields['country'].help_text = 'Pick your country from the list.'
        self.fields['city'].help_text = 'Provide your city.'
        self.fields['bio'].help_text = 'Tell people what you want to archive here.'        
        self.fields['interests'].help_text = 'Provide your interests.'       

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