from django import forms
from .models import ImageModel


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']
