from drigan.forms import DriganModelForm
from django import forms
from dynamic_forms.models import DynamicFormField


class AddDynamicFormField(DriganModelForm):

    class Meta:
        model = DynamicFormField
        fields = ('name', 'field_type', 'required')


class AddChoices(forms.Form):

    name = forms.CharField(max_length=100)


class BaseDynamicForm(forms.Form):

    def __init__(self, dynamic_form, *args, **kwargs):
        super(BaseDynamicForm, self).__init__(*args, **kwargs)
        dynamic_fields = dynamic_form.fields
        for dynamic_field in dynamic_fields.all():
            self.fields[dynamic_field.name] = dynamic_field.get_django_field()
