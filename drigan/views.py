from datetime import datetime

from django.views.generic.list import ListView
from events.models import Event


class StartView(ListView):
    queryset = Event.objects.exclude(start_date__lt=datetime.now())\
                            .order_by('start_date')[:5]
    template_name = "start.html"
