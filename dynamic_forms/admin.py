from django.contrib import admin
from dynamic_forms.models import DynamicFormField, DynamicForm, DynamicFormData

admin.site.register(DynamicForm)
admin.site.register(DynamicFormField)
admin.site.register(DynamicFormData)
