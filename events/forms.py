from drigan.forms import DriganModelForm
from events.models import Event, Organizer, Attraction


class AddEventForm(DriganModelForm):
    error_css_class = "form-error"

    class Meta:
        model = Event
        fields = ('name',)


class EditEventForm(DriganModelForm):
    class Meta:
        model = Event
        fields = ('name', 'start_date', 'end_date',
                  'website', 'category', 'description')


class AddOrganizerForm(DriganModelForm):
    class Meta:
        model = Organizer
        fields = ('name', 'mail', 'phone', 'address')


class AddAttractionForm(DriganModelForm):
    class Meta:
        model = Attraction
        fields = ('name', 'start_date', 'end_date', 'place',
                  'description', 'category')
