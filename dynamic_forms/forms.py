from drigan.forms import DriganModelForm
from dynamic_forms.models import DynamicFormField


class AddDynamicFormField(DriganModelForm):

    class Meta:
        model = DynamicFormField
        fields = ('name', 'field_type', 'required')
