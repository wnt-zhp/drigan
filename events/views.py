from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http
from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from events.forms import AddOrganizerForm, EditOrganizerForm, \
    AddEventForm, EditEventForm, AddAttractionForm, ChangeEventLogoForm
from events.models import Event, Attraction


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    change_logo_form = ChangeEventLogoForm()
    return render_to_response("events/event_details.html",
                              {"event":             event,
                               "change_logo_form": change_logo_form,
                               },
                              context_instance=RequestContext(request))


@login_required
@transaction.commit_on_success
def add_event(request):
    if request.method == 'POST':
        form = AddEventForm(request.POST, prefix='event')
        organizer_form = AddOrganizerForm(request.POST, prefix='organizer')
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            if organizer_form.is_valid():
                organizer = organizer_form.save(commit=False)
                organizer.related_user = request.user
                organizer.save()
                organizer_form.save()
                event.organizer = organizer
                event.save()
                form.save()
                messages.success(request,
                                 _('Event has been added successfully.'))
                return http.HttpResponseRedirect(reverse(
                    'events.views.event_details',
                    args=(event.id,)))
    else:
        form = AddEventForm(prefix='event')
        organizer_form = AddOrganizerForm(prefix='organizer')
    return render_to_response("events/event_add.html",
                              {"form": form, "organizer_form": organizer_form},
                              context_instance=RequestContext(request))


@login_required
@transaction.commit_on_success
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    organizer = event.organizer
    if request.method == "POST":
        form = EditEventForm(request.POST, instance=event, prefix='event')
        organizer_form = EditOrganizerForm(request.POST,
                                           instance=organizer,
                                           prefix='organizer')
        if form.is_valid() and organizer_form.is_valid():
            event = form.save()
            organizer = organizer_form.save()
            messages.success(request,
                             _('Event has been changed successfully.'))
            return http.HttpResponseRedirect(reverse(
                'events.views.event_details',
                args=(event.id,)))
    else:
        form = EditEventForm(instance=event, prefix='event')
        organizer_form = EditOrganizerForm(instance=organizer,
                                           prefix='organizer')

    return render_to_response("events/event_edit.html",
                              {"form": form, "organizer_form": organizer_form,
                               "event": event},
                              context_instance=RequestContext(request))


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, _('Event has been deleted.'))
    return http.HttpResponseRedirect(reverse(add_event))


def change_event_logo(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=event_id)
        form = ChangeEventLogoForm(request.POST, request.FILES,
                                   instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,
                             _('Logo changed successfully'))
        else:
            messages.error(request,
                           _('Form data incorrect.'))
            messages.error(request, form.errors.as_text())
    else:
        messages.error(request,
                       _('Logo not changed - no data given.'))
    return http.HttpResponseRedirect(reverse(event_details, args=(event_id,)))


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
            messages.success(request,
                             _('Attraction has been added successfully.'))
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
    return render_to_response("events/attraction_details.html",
                              {"attraction": attraction},
                              context_instance=RequestContext(request))


@login_required
def edit_attraction(request, event_id, attraction_id):
    attraction = get_object_or_404(Attraction, pk=attraction_id)
    if request.method == "POST":
        form = AddAttractionForm(request.POST, instance=attraction)
        if form.is_valid():
            attraction = form.save()
            messages.success(request,
                             _('Attraction has been changed successfully.'))
            return http.HttpResponseRedirect(reverse(
                'events.views.attraction_details',
                args=(attraction.event.id, attraction.id,)))
    else:
        form = AddAttractionForm(instance=attraction)
    return render_to_response("events/attraction_edit.html",
                              {"form": form,
                               "attraction": attraction},
                              context_instance=RequestContext(request))


@login_required
def delete_attraction(request, event_id, attraction_id):
    attraction = get_object_or_404(Attraction, pk=attraction_id)
    event = attraction.event
    if request.method == "POST":
        attraction.delete()
        messages.success(request, _('Attraction has been deleted.'))
    return http.HttpResponseRedirect(reverse('events.views.event_details',
                                             args=(event.id,)))
