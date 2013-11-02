from django.conf.urls import patterns
from dynamic_forms import views

urlpatterns = patterns('',
    (r'^add/(?P<dynamic_form_id>\d+)/$', views.add_dynamic_form_field),
    (r'^fill/(?P<dynamic_form_id>\d+)/$', views.fill_form),
    (r'^add/(?P<content_type_model>[-\w]+)/(?P<object_id>\d+)/$',
     views.add_dynamic_form),
)
