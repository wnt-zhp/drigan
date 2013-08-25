from django.conf.urls import patterns, include, url
from events import views

urlpatterns = patterns('',
    (r'^(?P<event_id>\d+)/$', views.event_details),
    (r'^add/$', views.add_event),
)
