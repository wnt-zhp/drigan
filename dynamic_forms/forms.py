from drigan.forms import DriganModelForm
from django import forms
from dynamic_forms.models import DynamicFormField


types = {'IntegerField': forms.IntegerField(),
         'CharField': forms.CharField(max_length=100),
         'TextField': forms.CharField(widget=forms.Textarea),
         'EmailField': forms.EmailField(),
         'DateField': forms.DateField(),
         'BooleanField': forms.BooleanField()
         }


class AddDynamicFormField(DriganModelForm):

    class Meta:
        model = DynamicFormField
        fields = ('name', 'field_type', 'required')


class BaseDynamicForm(forms.Form):

    def __init__(self, dynamic_form, *args, **kwargs):
        super(BaseDynamicForm, self).__init__(*args, **kwargs)
        dynamic_fields = dynamic_form.fields
        for dynamic_field in dynamic_fields.all():
            field_type = types[dynamic_field.field_type]
            field_type.required = dynamic_field.required
            self.fields[dynamic_field.name] = field_type
