from events.models import Event, Attraction, Organizer, \
    SportCategory, AttractionCategory, CategoryAdmin
from django.contrib import admin

admin.site.register(Event)
admin.site.register(Attraction)
admin.site.register(Organizer)
admin.site.register(SportCategory, CategoryAdmin)
admin.site.register(AttractionCategory, CategoryAdmin)
