from django import forms
from django.forms import ModelForm
from events.models import Event

class AddEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('organizer')
