from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.forms import *
from events.models import *


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    all_attractions = Attraction.objects.all().filter(event=event)
    organizer = Organizer.objects.get(event=event)
    return render_to_response("events/event_details.html",
                              {"event": event,
                               "all_attractions": all_attractions,
                               "organizer": organizer},
                              context_instance=RequestContext(request))


@login_required
def add_event(request):
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        organizer_form = AddOrganizerForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save()
            if organizer_form.is_valid():
                organizer = organizer_form.save(commit=False)
                organizer.event = event
                organizer.save()
                organizer_form.save()
                return http.HttpResponseRedirect(reverse(
                    'events.views.event_details',
                    args=(event.id,)))
    else:
        form = AddEventForm()
        organizer_form = AddOrganizerForm()
    return render_to_response("events/event_add.html",
                              {"form": form, "organizer_form": organizer_form},
                              context_instance=RequestContext(request))


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    organizer = Organizer.objects.get(event=event)
    if request.method == "POST":
        form = EditEventForm(request.POST, instance=event)
        organizer_form = AddOrganizerForm(request.POST,
                                          instance=organizer)
        if form.is_valid():
            event = form.save()
            if organizer_form.is_valid():
                organizer = organizer_form.save()
                return http.HttpResponseRedirect(reverse(
                    'events.views.event_details',
                    args=(event.id,)))
    else:
        form = EditEventForm(instance=event)
        organizer_form = AddOrganizerForm(instance=organizer)

    return render_to_response("events/event_edit.html",
                              {"form": form, "organizer_form": organizer_form,
                               "event": event},
                              context_instance=RequestContext(request))


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.success(request, 'Event has been deleted.')
    return http.HttpResponseRedirect('/')


@login_required
def add_attraction(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = AddAttractionForm(request.POST)
        if form.is_valid():
            attraction = form.save(commit=False)
            attraction.event = event
            attraction.save()
            form.save()
            return http.HttpResponseRedirect(reverse(
                'events.views.attraction_details',
                args=(event.id, attraction.id,)))
    else:
        form = AddAttractionForm()
    return render_to_response("events/attraction_add.html",
                              {"form": form},
                              context_instance=RequestContext(request))


def attraction_details(request, event_id, attraction_id):
    attraction = get_object_or_404(Attraction, id=attraction_id)
    event = get_object_or_404(Event, pk=event_id)
    return render_to_response("events/attraction_details.html",
                              {"attraction": attraction, "event": event},
                              context_instance=RequestContext(request))


@login_required
def edit_attraction(request, event_id, attraction_id):
    attraction = get_object_or_404(Attraction, pk=attraction_id)
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = AddAttractionForm(request.POST, instance=attraction)
        if form.is_valid():
            attraction = form.save()
            return http.HttpResponseRedirect(reverse(
                'events.views.attraction_details',
                args=(event.id, attraction.id,)))
    else:
        form = AddAttractionForm(instance=attraction)
    return render_to_response("events/attraction_edit.html",
                              {"form": form, "event": event,
                               "attraction": attraction},
                              context_instance=RequestContext(request))


@login_required
def delete_attraction(request, event_id, attraction_id):
    attraction = get_object_or_404(Attraction, pk=attraction_id)
    event = get_object_or_404(Event, pk=event_id)
    attraction.delete()
    messages.success(request, 'Attraction has been deleted.')
    return http.HttpResponseRedirect(reverse('events.views.event_details',
                                             args=(event.id,)))
