from django import forms
from posts.models import post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title', 'description', 'attachment']

