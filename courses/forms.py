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
    def get_tutor_courses(self):
        return self.user.tutor_courses

    course = forms.ModelChoiceField(queryset=Course.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SectionForm, self).__init__(*args, **kwargs)
        if user is not None:
            tutor_courses = user.tutor_courses.all()
            self.fields['course'].queryset = tutor_courses
            if not tutor_courses:
                self.fields['course'].help_text = "You need to <b>create</b> a course to create sections in it"

    class Meta:
        model = CourseSections
        fields = ('title','course')

class SectionVideoForm(forms.ModelForm):
    section = forms.ModelChoiceField(queryset=CourseSections.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SectionVideoForm, self).__init__(*args, **kwargs)
        if user is not None:
            creator_sections = user.creator_sections.all()
            self.fields['section'].queryset = creator_sections

            if not creator_sections:
                self.fields['section'].help_text = "You need to <b>create</b> a section to add videos in it"

    class Meta:
        model = SectionVideos
        fields = ('section','video')

