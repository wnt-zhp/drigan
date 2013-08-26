from django import forms
from django.forms import ModelForm
from events.models import Event, Organizer, Attraction


class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'event_start_date',
                  'event_end_date', 'event_website', 'categories')


class EditEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'event_start_date', 'event_end_date',
                  'event_website', 'categories', 'event_description')


class AddOrganizerForm(ModelForm):
    class Meta:
        model = Organizer
        fields = ('organizer_name', 'organizer_mail', 'organizer_phone')


class AddAttractionForm(ModelForm):
    class Meta:
        model = Attraction
        fields = ('attraction_name', 'attraction_start_date',
                  'attraction_end_date', 'attraction_place',
                  'attraction_description', 'attraction_categories')
