from drigan.forms import DriganModelForm
from DynamicForms.models import DynamicFormField


class AddDynamicFormField(DriganModelForm):

    class Meta:
        model = DynamicFormField
        fields = ('name', 'field_type', 'required')
