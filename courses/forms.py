from django import forms
from .models import Course,CourseSections,SectionVideos,Review
import subprocess
from django.shortcuts import get_object_or_404

class SearchStudentForm(forms.Form):
    query = forms.CharField(max_length=200)

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
    image = forms.ImageField(required=True)
    cover = forms.ImageField(required=False)
    preview_video = forms.FileField(label='You can add a preview video, that will show main idea of your course',required=False)
    thumbnails = forms.ImageField(required=False)


    class Meta:
        model = Course
        fields = ('image','cover','languages','price','preview_video','poster_preview_video')

    # def save(self):

    #     subprocess.call(" ffmpeg -i"+ uploaded_filename +"-ss 00:00:01.000 -vframes 1 "+thumbnail_name ,shell=True)


class SectionForm(forms.ModelForm):
    def get_tutor_courses(self):
        return self.user.tutor_courses

    # course = forms.ModelChoiceField(queryset=Course.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SectionForm, self).__init__(*args, **kwargs)
        if user is not None:
            tutor_courses = user.tutor_courses.all()
            # self.fields['course'].queryset = tutor_courses
            self.fields['title'].widget.attrs.update({'id':'title_section'})
            if not tutor_courses:
                self.fields['course'].help_text = "You need to <b>create</b> a course to create sections in it"

    class Meta:
        model = CourseSections
        fields = ('title',)

class SectionVideoForm(forms.ModelForm):

    section = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SectionVideoForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'id':'title_video'})
        if user is not None:
            creator_sections = user.creator_sections.all()
            self.fields['section'].queryset = creator_sections
            # self.fields['section'].widget.attrs.update({'class':'noselection'})


            if not creator_sections:
                self.fields['section'].help_text = "You need to <b>create</b> a section to add videos in it"

    class Meta:
        model = SectionVideos
        fields = ('title','section','video')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)