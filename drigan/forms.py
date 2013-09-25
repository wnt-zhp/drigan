from django.forms import Form, ModelForm


class DriganForm(Form):
    error_css_class = "form-error"


class DriganModelForm(ModelForm):
    error_css_class = "form-error"
