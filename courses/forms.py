from django import forms
from .models import Course,CourseSections,SectionVideos




class SearchStudentForm(forms.Form):
    student_query = forms.CharField(max_length=200)
    


class CheckoutForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder':'Provide your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Provide your last name'})
        
class CourseForm1(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title',)
        # self.fields['title'].widget.attrs.update()

class CourseForm2(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('description',)

class CourseForm3(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('category',)

class CourseForm4(forms.ModelForm):
    image = forms.ImageField(required=False)
    cover = forms.ImageField(required=False)
    class Meta:
        model = Course
        fields = ('image','cover','languages','price',)

class SectionForm(forms.ModelForm):
    class Meta:
        model = CourseSections
        fields = ('title','course')

class SectionVideoForm(forms.ModelForm):
    class Meta:
        model = SectionVideos
        fields = ('section','video')

