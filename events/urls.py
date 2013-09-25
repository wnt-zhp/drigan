from django.conf.urls import patterns, url
from events import views

urlpatterns = patterns('',
    (r'^(?P<event_id>\d+)/$', views.event_details),
    (r'^edit/(?P<event_id>\d+)/$', views.edit_event),
    (r'^delete/(?P<event_id>\d+)/$', views.delete_event),
    (r'^add/$', views.add_event),
    (r'^change_logo/(?P<event_id>\d+)/$', views.change_event_logo),
    (r'^(?P<event_id>\d+)/attractions/(?P<attraction_id>\d+)/$',
     views.attraction_details),
    (r'^(?P<event_id>\d+)/attractions/add/$', views.add_attraction),
    (r'^(?P<event_id>\d+)/attractions/edit/(?P<attraction_id>\d+)/$',
     views.edit_attraction),
    (r'^(?P<event_id>\d+)/attractions/delete/(?P<attraction_id>\d+)/$',
     views.delete_attraction),
)
