from django.contrib import admin
from dynamic_forms.models import DynamicFormField, DynamicForm

admin.site.register(DynamicForm)
admin.site.register(DynamicFormField)
