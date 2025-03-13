from django import forms
from .models import upload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = upload
        fields = ['image']
