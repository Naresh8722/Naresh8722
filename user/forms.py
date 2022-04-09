from django import forms
from .models import StaticSubscribe

class CommentForm(forms.ModelForm):
    class Meta:
        model=StaticSubscribe
        fields="__all__"