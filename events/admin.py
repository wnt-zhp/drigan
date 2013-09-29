from events.models import Event, Attraction, Organizer, AttractionCategory,\
    SportCategory, SerialEventGroup
from django.contrib import admin

admin.site.register(Event)
admin.site.register(Attraction)
admin.site.register(Organizer)
admin.site.register(SerialEventGroup)
admin.site.register(AttractionCategory)
admin.site.register(SportCategory)
