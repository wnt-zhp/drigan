from events.models import *
from django.contrib import admin

admin.site.register(Event)
admin.site.register(Attraction)
admin.site.register(Organizer)
admin.site.register(SportCategory, CategoryAdmin)
admin.site.register(AttractionCategory, CategoryAdmin)
