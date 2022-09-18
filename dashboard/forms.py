from django import forms
from .models import Courses


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['Title', 'Course_code', 'Enroll_key']
