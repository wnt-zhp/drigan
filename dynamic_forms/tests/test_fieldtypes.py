from django.forms.fields import IntegerField
from django.forms.widgets import Textarea

# Create your tests here.

from unittest import TestCase
from dynamic_forms.models import DynamicFormField, DynamicForm

from ..fieldtype import get_field, get_field_type_choices, DynamicFieldController, register_field_type


class TestFieldtype(TestCase):

    def test_field_properly_constructed(self):

        field = get_field("DynamicIntegerField")

        f = field._create_field()

        self.assertIsInstance(f, IntegerField)

    def test_register_works(self):

        @register_field_type("__TEST")
        class TestField(DynamicFieldController):

            def get_type_description(self):
                return "__TEST_DESCRIPTION"

            def _create_field(self):
                return None

        self.assertIsInstance(get_field("__TEST"), TestField)
        self.assertIn(("__TEST", "__TEST_DESCRIPTION"), get_field_type_choices())

    def test_text_field(self):

        field = get_field("DynamicTextField")

        f = field._create_field()

        self.assertIsInstance(f.widget, Textarea)

    def test_load_field(self):

        form = DynamicForm.objects.create()

        dynamic = DynamicFormField.objects.create(
            name="Foo",
            field_type="DynamicIntegerField",
            required=False,
            form=form
        )

        field = dynamic.get_django_field()

        self.assertIsInstance(field, IntegerField)
        self.assertFalse(field.required)


class TestDynamicFieldTypeBehaviour(TestCase):

    class DynamicFieldTypeDefault(DynamicFieldController):

        def get_type_description(self):
            return super().get_type_description()

        def _create_field(self):
            return super()._create_field()

    def test_get_description(self):
        self.assertIsNone(self.DynamicFieldTypeDefault().get_type_description())

    def test_create_field(self):
        self.assertIsNone(self.DynamicFieldTypeDefault()._create_field())
