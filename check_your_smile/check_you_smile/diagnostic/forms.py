from django import forms
from .models import PhotoDiagnostic
from result.models import ResultDiagnostic

class PhotoDiagnosticForm(forms.ModelForm):
    class Meta:
        model = PhotoDiagnostic
        fields = ('name', 'image_lateral', 'image_frontal')


class ResultDiagnosticForm(forms.ModelForm):
    class Meta:
        model = ResultDiagnostic
        fields = ()

