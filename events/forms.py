from django import forms
from django.forms import ModelForm
from events.models import Event, Organizer, Attraction


class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name',)


class EditEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'start_date', 'end_date',
                  'website', 'category', 'description')


class AddOrganizerForm(ModelForm):
    class Meta:
        model = Organizer
        fields = ('name', 'mail', 'phone', 'address')


class AddAttractionForm(ModelForm):
    class Meta:
        model = Attraction
        fields = ('name', 'start_date', 'end_date', 'place',
                  'description', 'category')
