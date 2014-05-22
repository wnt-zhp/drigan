from django.conf.urls import patterns, url
from events import views
from events.models import Event, Attraction

urlpatterns = patterns('',
    url(r'^(?P<event_id>\d+)/$', views.event_details,
        name='events-event-details'),
    url(r'^edit/(?P<event_id>\d+)/$', views.edit_event,
        name='events-edit-event'),
    url(r'^delete/(?P<event_id>\d+)/$', views.delete_event,
        name='events-delete-event'),
    url(r'^add/$', views.add_event,
        name='events-add-event'),
    url(r'^change_logo/(?P<object_id>\d+)/$', views.change_logo,
        {'model_cls': Event, 'reverse_view': views.event_details},
        name='events-change-event-logo'),
    url(r'^change_logo/attraction/(?P<object_id>\d+)/$', views.change_logo,
        {'model_cls': Attraction, 'reverse_view': views.attraction_details},
        name='events-change-attraction-logo'),
    url(r'^attractions/(?P<attraction_id>\d+)/$', views.attraction_details,
        name='events-attraction-details'),
    url(r'^(?P<event_id>\d+)/attractions/add/$', views.add_attraction,
        name='events-add-attraction'),
    url(r'^(?P<event_id>\d+)/attractions/edit/(?P<attraction_id>\d+)/$',
        views.edit_attraction, name='events-edit-attraction'),
    url(r'^(?P<event_id>\d+)/attractions/delete/(?P<attraction_id>\d+)/$',
        views.delete_attraction, name='events-delete-attraction'),
)
