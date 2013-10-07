from django.contrib import admin
from DynamicForms.models import DynamicFormField, DynamicForm

admin.site.register(DynamicForm)
admin.site.register(DynamicFormField)
