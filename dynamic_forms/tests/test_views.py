# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from dynamic_forms.fieldtype import get_field_type_choices
from dynamic_forms.models import DynamicForm, DynamicFormField, DynamicFormData


class AddDynamicFormTest(TestCase):
    fixtures = [
        'dynamic-forms-test-users.json',
    ]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.assertTrue(self.client.login(username='test', password='test'))

    def __add_dynamic_form(self, attached_model, validate_response=True):
        ct = ContentType.objects.get_for_model(attached_model)
        # We need to attach something. So let;s attach user :)
        response = self.client.post(
            reverse("dynamic_forms.views.add_dynamic_form", kwargs={
                "content_type_model": ct.name,
                "object_id": attached_model.pk
            })
        )
        if validate_response:
            self.assertEqual(response.status_code, 302)
        return response

    def test_add_form(self):
        # No forms in fixture
        self.assertEqual(DynamicForm.objects.all().count(), 0)

        test_user = get_user_model().objects.get(username="test")

        self.__add_dynamic_form(test_user)

        # Form created
        self.assertEqual(DynamicForm.objects.all().count(), 1)
        df = DynamicForm.objects.all()[0]
        # Form points to appropriate object
        self.assertEqual(df.content_object, test_user)

    def test_add_form_no_remote_object(self):
        # No forms in fixture
        self.assertEqual(DynamicForm.objects.all().count(), 0)
        # Assert that there is no such user in the database
        self.assertEqual(get_user_model().objects.filter(pk=666).count(), 0)
        no_such_user = get_user_model()(pk=666)
        response = self.__add_dynamic_form(no_such_user,
                                           validate_response=False)

        # Should return 404
        self.assertEqual(response.status_code, 404)
        # And create no objects
        self.assertEqual(DynamicForm.objects.all().count(), 0)


class AddFieldTests(TestCase):
    fixtures = [
        'dynamic-forms-test-users.json',
    ]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.assertTrue(self.client.login(username='test', password='test'))
        self.dynamic_form = DynamicForm.objects.create()

    def test_add_form_field(self):
        self.assertEqual(DynamicFormField.objects.all().count(), 0)
        form_add_field_url = reverse(
            "dynamic_forms.views.add_dynamic_form_field",
            kwargs={'dynamic_form_id': self.dynamic_form.pk})
        response = self.client.post(
            form_add_field_url,
            data={
                "name": "test",
                "required": "on",
                "field_type": "DynamicIntegerField"
            })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith(form_add_field_url))
        self.assertEqual(DynamicFormField.objects.all().count(), 1)
        df = DynamicFormField.objects.all()[0]
        self.assertEqual(df.name, "test")
        self.assertTrue(df.required)
        self.assertEqual(df.field_type, "DynamicIntegerField")

    def test_add_form_field_invalid_type(self):
        self.assertEqual(DynamicFormField.objects.all().count(), 0)
        self.assertNotIn("NoSuchType", get_field_type_choices())
        response = self.client.post(
            reverse("dynamic_forms.views.add_dynamic_form_field",
                    kwargs={'dynamic_form_id': self.dynamic_form.pk}),
            data={
                "name": "test",
                "required": "on",
                "field_type": "NoSuchType"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DynamicFormField.objects.all().count(), 0)

    def test_add_form_field_field_name_not_unique(self):
        DynamicFormField.objects.create(
            name="test", required=True, field_type="DynamicIntegerField",
            form=self.dynamic_form)

        self.assertEqual(DynamicFormField.objects.all().count(), 1)
        response = self.client.post(
            reverse("dynamic_forms.views.add_dynamic_form_field",
                    kwargs={'dynamic_form_id': self.dynamic_form.pk}),
            data={
                "name": "test",
                "required": "on",
                "field_type": "DynamicIntegerField"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DynamicFormField.objects.all().count(), 1)

    def test_add_choice(self):
        self.assertEqual(DynamicFormField.objects.all().count(), 0)

        form_add_field_url = reverse(
            "dynamic_forms.views.add_dynamic_form_field",
            kwargs={'dynamic_form_id': self.dynamic_form.pk})

        response = self.client.post(
            form_add_field_url,
            data={
                "name": "test",
                "required": "on",
                "field_type": "DynamicChoicesField"
            })

        self.assertEqual(response.status_code, 302)

        self.assertEqual(DynamicFormField.objects.all().count(), 1)
        df = DynamicFormField.objects.all()[0]
        self.assertEqual(df.name, "test")
        self.assertTrue(df.required)
        self.assertEqual(df.field_type, "DynamicChoicesField")

        redirect = reverse(
            "dynamic_forms.views.add_choices_to_choicefield",
            kwargs={'field_id': df.pk}
        )

        self.assertTrue(
            response['Location'].endswith(redirect),
            "Response does not redirect to expected location '{}' but to {}".format(
                redirect, response["Location"]
            ))


class AddChoicesToChoiceField(TestCase):
    fixtures = [
        'dynamic-forms-test-users.json',
    ]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.assertTrue(self.client.login(username='test', password='test'))
        self.dynamic_form = DynamicForm.objects.create()
        self.dynamic_field = DynamicFormField.objects.create(
            form=self.dynamic_form,
            field_type="DynamicChoicesField",
            name="test_choice"
        )

        self.add_choice_url = reverse(
            "dynamic_forms.views.add_choices_to_choicefield",
            kwargs={'field_id': self.dynamic_field.pk}
        )

    def test_add_new_choice_field(self):
        df = DynamicFormField.objects.get(pk=self.dynamic_field.pk)

        self.assertEqual(len(df.dynamic_field.get_choices(df)), 0)

        response = self.client.post(self.add_choice_url, data={
            "name": "foobar"
        })

        self.assertEqual(response.status_code, 302)

        df = DynamicFormField.objects.get(pk=self.dynamic_field.pk)

        self.assertEqual(len(self.dynamic_field.dynamic_field.get_choices(df)),
                         1)

        self.assertTrue(response['Location'].endswith(self.add_choice_url))

    def test_add_new_choice_field_twice(self):
        choices = self.dynamic_field.dynamic_field.get_choices(
            self.dynamic_field)
        self.assertEqual(len(choices), 0)

        self.dynamic_field.dynamic_field.add_choice(self.dynamic_field, "foo")
        self.dynamic_field.save()

        response = self.client.post(self.add_choice_url, data={
            "name": "foo"
        })

        self.assertEqual(response.status_code, 200)

        df = DynamicFormField.objects.get(pk=self.dynamic_field.pk)

        self.assertEqual(len(self.dynamic_field.dynamic_field.get_choices(df)),
                         1)


class TestBasicFormBase(object):
    fixtures = [
        'dynamic-forms-test-users.json',
    ]

    def setUp(self):
        self.client = Client()
        self.assertTrue(self.client.login(username='test', password='test'))
        self.dynamic_form = DynamicForm.objects.create()
        self.dynamic_field_1 = DynamicFormField.objects.create(
            form=self.dynamic_form,
            field_type="IntegerField",
            name="First"
        )
        self.dynamic_field_2 = DynamicFormField.objects.create(
            form=self.dynamic_form,
            field_type="IntegerField",
            name="Second"
        )


class TestEditForm(TestBasicFormBase, TestCase):
    def test_delete(self):
        self.assertEqual(
            DynamicFormField.objects.filter(form=self.dynamic_form).count(), 2)
        response = self.client.post(
            reverse("dynamic_forms.views.delete_dynamic_form_field",
                    kwargs={'field_id': self.dynamic_field_1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            DynamicFormField.objects.filter(form=self.dynamic_form).count(), 1)

    def test_initial_order(self):
        self.assertEqual(
            list(self.dynamic_form.fields.all()),
            [self.dynamic_field_1, self.dynamic_field_2]
        )

    def test_change_order(self):
        response = self.client.post(
            reverse("dynamic_forms.views.change_field_order",
                    kwargs={
                        "field_id": self.dynamic_field_1.pk,
                        "direction": "-1"
                    }))

        self.assertEqual(response.status_code, 302)

        redirect_target = reverse(
            'dynamic_forms.views.edit_dynamic_form',
            kwargs={"dynamic_form_id": self.dynamic_form.pk}
        )

        self.assertTrue(response['Location'].endswith(redirect_target))

        self.assertEqual(
            list(self.dynamic_form.fields.all()),
            [self.dynamic_field_2, self.dynamic_field_1]
        )


class TestFillForm(TestCase):
    fixtures = [
        'dynamic-forms-test-users.json',
    ]

    def setUp(self):
        self.client = Client()
        self.assertTrue(self.client.login(username='test', password='test'))
        self.dynamic_form = DynamicForm.objects.create()
        self.dynamic_field_1 = DynamicFormField.objects.create(
            form=self.dynamic_form,
            field_type="DynamicIntegerField",
            name="First",
            required=False
        )
        self.dynamic_field_2 = DynamicFormField.objects.create(
            form=self.dynamic_form,
            field_type="DynamicCharField",
            name="Second",
            required=True
        )
        self.dynamic_field_3 = DynamicFormField.objects.create(
            form=self.dynamic_form,
            field_type="DynamicChoicesField",
            name="Third",
            required=False
        )

        self.dynamic_field_3.dynamic_field.add_choice(self.dynamic_field_3,
                                                      "foo")
        self.dynamic_field_3.dynamic_field.add_choice(self.dynamic_field_3,
                                                      "bar")
        self.dynamic_field_3.save()

        self.fill_form_url = reverse("dynamic_forms.views.fill_form",
                                     kwargs={
                                         "dynamic_form_id": self.dynamic_form.pk})

        self.participants_url = reverse(
            "dynamic_forms.views.participants_list",
            kwargs={"dynamic_form_id": self.dynamic_form.pk})

    def test_fill_ok(self):
        self.assertEqual(DynamicFormData.objects.all().count(), 0)
        response = self.client.post(
            self.fill_form_url,
            data={
                "First": "21342123",
                "Second": "SelectedOption",
                "Third": "foo"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith(self.participants_url))
        self.assertEqual(DynamicFormData.objects.all().count(), 1)

    def __make_bad_request_test(self, data):
        self.assertEqual(DynamicFormData.objects.all().count(), 0)
        response = self.client.post(
            self.fill_form_url,
            data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(DynamicFormData.objects.all().count(), 0)

    def test_fill_bad_type(self):
        self.__make_bad_request_test({
            "First": "dupa",
            "Second": "Das",
            "Third": "foo"
        })

    def test_fill_miss_required(self):
        self.__make_bad_request_test({
            "First": "dupa",
            "Third": "foo"
        })

    def test_fill_invalid_choice(self):
        self.__make_bad_request_test({
            "First": "dupa",
            "Second": "Das",
            "Third": "NoSuchChoice"
        })

    def test_participants(self):
        self.client.post(
            self.fill_form_url,
            data={
                "First": "21342123",
                "Second": "SelectedOption",
                "Third": "foo"
            }
        )

        response = self.client.get(self.participants_url)

        self.assertIn(b"21342123", response.content)
        self.assertIn(b"SelectedOption", response.content)
        self.assertIn(b"foo", response.content)
