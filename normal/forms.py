from django import forms
from normal.models import Message


class MessageForm(forms.ModelForm):

    class Meta():
        model = Message
        fields = {'title','msg'}
