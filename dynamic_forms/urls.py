from django.conf.urls import patterns
from dynamic_forms import views

urlpatterns = patterns('',
    (r'^add/(?P<dynamic_form_id>\d+)/$', views.add_dynamic_form_field),
    (r'^edit/(?P<dynamic_form_id>\d+)/$', views.edit_dynamic_form),
    (r'^delete_field/(?P<field_id>\d+)$', views.delete_dynamic_form_field),
    (r'^change_order/(?P<field_id>\d+)/(?P<direction>-?\d+)/$',
     views.change_field_order),
    (r'^add/choice/(?P<field_id>\d+)/$', views.add_choices_to_choicefield),
    (r'^fill/(?P<dynamic_form_id>\d+)/$', views.fill_form),
    (r'^add/(?P<content_type_model>[-\w]+)/(?P<object_id>\d+)/$',
     views.add_dynamic_form),
    (r'^list/(?P<dynamic_form_id>\d+)/$', views.participants_list),
)
