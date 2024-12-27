from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'category', 'sensitivity', 'visibility']

class DocumentSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Title')
    category = forms.CharField(required=False, label='Category')
    status = forms.CharField(required=False, label='Status')