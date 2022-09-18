from django import forms
from assignment.models import Assignment, AssignmentAns


class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['Title', 'Question', 'image', 'file', 'last_date_of_submission']


class AssignmentAnsForm(forms.ModelForm):
    class Meta:
        model = AssignmentAns
        fields = ['answer', 'ans_file']

