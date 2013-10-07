from django.conf.urls import patterns
from DynamicForms import views

urlpatterns = patterns('',
    (r'^add/(?P<dynamic_form_id>\d+)/$', views.add_dynamic_form_field),
    (r'^add/(?P<content_type_model>[-\w]+)/(?P<object_id>\d+)/$',
     views.add_dynamic_form),
)
