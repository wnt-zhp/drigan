from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class PermissionsTest(TestCase):
    """
    This TestCase tests all views in this module for correct permissions
    handling (i.e. returning 403 on pages that the user has no access to
    and redirecting to login page when it's needed.
    """

    def setUp(self):
        User.objects.create_user(
            username='fred', email='fred@example.com', password='secret')

    def test_StartView(self):
        """
        This TestCase just tests if both not logged in user can access
        the main page.
        """
        response = Client().get(reverse("drigan-start"))
        self.assertEqual(response.status_code, 200)

        c = Client()
        c.login(username='fred', password='secret')
        response = Client().get(reverse("drigan-start"))
        self.assertEqual(response.status_code, 200)
