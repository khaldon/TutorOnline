from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    price = forms.CharField(required=False)

    class Meta:
        model = Course
        fields = ('title','description','section','image','cover','category','languages','price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder':'Write course title'})
        self.fields['description'].widget.attrs.update({'placeholder':'Describe your course'})
        self.fields['price'].widget.attrs.update({'placeholder':'Write the price if that needed'})

class CheckoutForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder':'Provide your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Provide your last name'})
        