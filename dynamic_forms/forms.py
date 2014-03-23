from drigan.forms import DriganModelForm
from django import forms
from dynamic_forms.models import DynamicFormField


types = {'IntegerField': forms.IntegerField,
         'CharField': forms.CharField,
         'TextField': forms.CharField,
         'EmailField': forms.EmailField,
         'DateField': forms.DateField,
         'BooleanField': forms.BooleanField,
         'ChoiceField': forms.ChoiceField
         }


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
            field_type = types[dynamic_field.field_type]
            field = field_type()
            field.required = dynamic_field.required
            if dynamic_field.field_type == 'TextField':
                field.widget = forms.Textarea()
            if dynamic_field.field_type == 'ChoiceField':
                if not dynamic_field.required:
                    blank_choice = {'': '---------'}
                    all_choices = dynamic_field.choices.copy()
                    all_choices.update(blank_choice)
                    dynamic_field.choices = all_choices
                field.choices = list(dynamic_field.choices.items())
            self.fields[dynamic_field.name] = field
