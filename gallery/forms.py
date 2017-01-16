# -*- coding: utf-8 -*-

from django import forms


class ImageForm(forms.Form):
    docfile = forms.ImageField(
        label='Select a file'
    )
'''

from django.db import models
from django.forms import ModelForm
from .models import Images


# FileUpload form class.
class ImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ('imgfile', 'description')
'''