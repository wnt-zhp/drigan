# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from dynamic_forms.models import DynamicForm


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
        response =  self.client.post(
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
        response = self.__add_dynamic_form(no_such_user, validate_response=False)

        #Should return 404
        self.assertEqual(response.status_code, 404)
        # And create no objects
        self.assertEqual(DynamicForm.objects.all().count(), 0)
