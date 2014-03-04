from django.conf.urls import patterns, url
from events import views
from events.models import Event, Attraction

urlpatterns = patterns('',
    (r'^(?P<event_id>\d+)/$', views.event_details),
    (r'^edit/(?P<event_id>\d+)/$', views.edit_event),
    (r'^delete/(?P<event_id>\d+)/$', views.delete_event),
    (r'^add/$', views.add_event),
    url(r'^change_logo/(?P<object_id>\d+)/$', views.change_logo,
        {'model_cls': Event, 'reverse_view': views.event_details},
        name='events-change-event-logo'),
    url(r'^change_logo/attraction/(?P<object_id>\d+)/$', views.change_logo,
        {'model_cls': Attraction, 'reverse_view': views.attraction_details},
        name='events-change-attraction-logo'),
    (r'^attractions/(?P<attraction_id>\d+)/$',
     views.attraction_details),
    (r'^(?P<event_id>\d+)/attractions/add/$', views.add_attraction),
    (r'^(?P<event_id>\d+)/attractions/edit/(?P<attraction_id>\d+)/$',
     views.edit_attraction),
    (r'^(?P<event_id>\d+)/attractions/delete/(?P<attraction_id>\d+)/$',
     views.delete_attraction),
)
