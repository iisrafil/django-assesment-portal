from django import forms
from django.forms import formset_factory
from PdfConverter.models import PdfFile


class PdfForm(forms.ModelForm):
    class Meta:
        model = PdfFile
        fields = ['name']


class ImageForm(forms.Form):
    name = forms.ImageField(
        label='Image',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        })
    )


ImageFormset = formset_factory(ImageForm, extra=1)

