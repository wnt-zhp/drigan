from django.shortcuts import render_to_response
from django.template import Context, RequestContext

def add_event(request):
    return render_to_response("events/event_add.html", context_instance=RequestContext(request))
