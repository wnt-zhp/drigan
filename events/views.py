from django import http
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from events.forms import AddEventForm
from events.models import Event


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render_to_response("events/event_details.html",
                              {"event": event},
                              context_instance=RequestContext(request))


@login_required
def add_event(request):

    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save()
            return http.HttpResponseRedirect(
                reverse('events.views.event_details', args=(event.id,)))
    else:
        form = AddEventForm()
    return render_to_response("events/event_add.html",
                              {"form": form},
                              context_instance=RequestContext(request))
