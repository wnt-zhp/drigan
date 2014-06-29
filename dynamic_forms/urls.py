from django.conf.urls import patterns, url
from dynamic_forms import views

urlpatterns = patterns('',
    url(r'^add/choice/(?P<field_id>\d+)/$',
        views.AddChoicesToChoiceField.as_view(),
        name="dynamic_forms.views.add_choices_to_choicefield"),
    url(r'^add/(?P<dynamic_form_id>\d+)/$',
        views.AddDynamicFormFieldView.as_view(),
        name="dynamic_forms.views.add_dynamic_form_field"),
    url(r'^add/(?P<content_type_model>[-\w]+)/(?P<object_id>\d+)/$',
        views.AddDynamicForm.as_view(),
        name="dynamic_forms.views.add_dynamic_form"),
    url(r'^edit/(?P<dynamic_form_id>\d+)/$',
        views.EditDynamicForm.as_view(),
        name="dynamic_forms.views.edit_dynamic_form"),
    url(r'^delete_field/(?P<field_id>\d+)$',
        views.DeleteDynamicFormField.as_view(),
        name="dynamic_forms.views.delete_dynamic_form_field"),
    url(r'^change_order/(?P<field_id>\d+)/(?P<direction>-?\d+)/$',
        views.ChangeFieldOrder.as_view(),
        name="dynamic_forms.views.change_field_order"),
    url(r'^fill/(?P<dynamic_form_id>\d+)/$',
        views.FillForm.as_view(),
        name='dynamic_forms.views.fill_form'),
    url(r'^list/(?P<dynamic_form_id>\d+)/$',
        views.ParticipantList.as_view(),
        name="dynamic_forms.views.participants_list")
)
