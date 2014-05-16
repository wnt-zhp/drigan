from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from events.models import Event, Attraction


class PermissionsTest(TestCase):
    """
    This TestCase tests all views in this module for correct permissions
    handling (i.e. returning 403 on pages that the user has no access to
    and redirecting to login page when it's needed.
    """

    def setUp(self):
        """
        Sets up two users:
            user1 -- creator of event1
            user2 -- just a normal user

        This has to be done through API, because we are testing if correct
        permissions are assigned.
        """
        self.user1_data = {
            'username': 'fred1',
            'email': 'fred@example.com',
            'password': 'secret',
        }
        self.user2_data = {
            'username': 'john2',
            'email': 'john@example.com',
            'password': 'secret',
        }
        User.objects.create_user(**self.user1_data)
        User.objects.create_user(**self.user2_data)

        c = Client()
        c.login(**self.user1_data)
        c.post(reverse('events-add-event'),
               {
                   'event-name': 'event1',
                   'event-category': '7',
                   'organizer-name': 'johnny',
                   'organizer-mail': 'john@example.com',
                   'organizer-phone': '555555',
               })

        self.event = Event.objects.get(name='event1')

        c = Client()
        c.login(**self.user1_data)
        c.post(reverse('events-add-attraction', args=(self.event.id,)),
               {
                   'name': 'attraction1',
                   'start_date': '2030-12-12',
                   'end_date': '2031-12-12',
                   'place': 'u-kingdom',
                   'description': 'john@example.com',
                   'category': '1',
               })

        self.attraction = Attraction.objects.get(name='attraction1')

    def assertAccessAllowed(self, url, user={}):
        """
        Asserts the user has access to given url using both POST and GET

        :param str: a url to test
        :param dict user: function will log in as user with given credentials
        """
        self.assertGETAccessAllowed(url, user)
        self.assertPOSTAccessAllowed(url, user)

    def assertGETAccessAllowed(self, url, user={}):
        """
        Asserts the user has access to given url using GET method

        :param str: a url to test
        :param dict user: function will log in as user with given credentials
        """
        c = Client()
        if "username" in user:
            c.login(**user)
        response = c.get(url)

        error_msg = "User '{}' does not have GET access to '{}'".format(
            user.get("username", "guest"),
            url)
        self.assertEqual(response.status_code, 200, error_msg)

    def assertPOSTAccessAllowed(self, url, user={}):
        """
        Asserts the user has access to given url by POST method

        :param str: a url to test
        :param dict user: function will log in as user with given credentials
        """
        c = Client()
        response = c.post(url)
        if response.status_code != 200:
            # if response is not 200 make sure that it redirects to url
            # different than login_url

            error_msg = "User '{}' does not have POST access to '{}'".format(
                user.get("username", "guest"),
                url)
            self.assertEqual(response.status_code, 302, error_msg)
            self.assertNotEqual(response.url,
                                settings.LOGIN_URL + "?next=" + url)

    def assertAccessDenied(self, url, user={}):
        """
        Asserts the user doesn't have access to given url

        :param str: a url to test
        :param dict user: function will log in as user with given credentials
        """
        c = Client()
        if "username" in user:
            c.login(**user)
        response = c.get(url)

        error_msg = "User '{}' does have access to '{}'".format(
            user.get("username", "guest"),
            url)

        if response.status_code == 302:
            self.assertRedirects(response, settings.LOGIN_URL + "?next=" + url,
                                 msg_prefix=error_msg)
        else:
            self.assertEqual(response.status_code, 405)  # forbidden

        response = c.post(url)
        if response.status_code == 302:
            self.assertRedirects(response, settings.LOGIN_URL + "?next=" + url,
                                 msg_prefix=error_msg)
        else:
            self.assertEqual(response.status_code, 405)  # forbidden

    def test_event_details_view(self):
        """
        All users should be able to see the event.
        """
        self.assertAccessAllowed(reverse('events-event-details',
                                         args=(self.event.id,)))
        self.assertAccessAllowed(reverse('events-event-details',
                                         args=(self.event.id,)),
                                 self.user2_data)
        self.assertAccessAllowed(reverse('events-event-details',
                                         args=(self.event.id,)),
                                 self.user1_data)

    def test_get_add_event_view(self):
        """
        Only logged in users should be able to see add event.
        """

        self.assertAccessDenied(reverse('events-add-event'))
        self.assertAccessAllowed(reverse('events-add-event'),
                                 self.user1_data)
        self.assertAccessAllowed(reverse('events-add-event'),
                                 self.user2_data)

    def test_edit_event_view(self):
        """
        Only event owner can edit event.
        """

        self.assertAccessDenied(reverse('events-edit-event',
                                        args=(self.event.id,)))
        self.assertAccessAllowed(reverse('events-edit-event',
                                         args=(self.event.id,)),
                                 self.user1_data)
        self.assertAccessDenied(reverse('events-edit-event',
                                        args=(self.event.id,)),
                                self.user2_data)

    def test_delete_event_view(self):
        """
        Only event owner can delete event.
        """

        self.assertAccessDenied(reverse('events-delete-event',
                                        args=(self.event.id,)))
        self.assertAccessDenied(reverse('events-delete-event',
                                        args=(self.event.id,)),
                                self.user2_data)
        self.assertPOSTAccessAllowed(reverse('events-delete-event',
                                             args=(self.event.id,)),
                                     self.user1_data)

    def test_change_event_logo_view(self):
        """
        Only event owner can change event logo.
        """

        self.assertAccessDenied(reverse('events-change-event-logo',
                                        args=(self.event.id,)))
        self.assertAccessDenied(reverse('events-change-event-logo',
                                        args=(self.event.id,)),
                                self.user2_data)
        self.assertPOSTAccessAllowed(reverse('events-change-event-logo',
                                             args=(self.event.id,)),
                                     self.user1_data)

    def test_change_attraction_logo_view(self):
        """
        Only event owner can change event attraction logo.
        """

        self.assertAccessDenied(reverse('events-change-attraction-logo',
                                        args=(self.attraction.id,)))
        self.assertAccessDenied(reverse('events-change-attraction-logo',
                                        args=(self.attraction.id,)),
                                self.user2_data)
        self.assertPOSTAccessAllowed(reverse('events-change-attraction-logo',
                                             args=(self.attraction.id,)),
                                     self.user1_data)

    def test_add_attraction_view(self):
        """
        Only event owner can add attractions.
        """

        self.assertAccessDenied(reverse('events-add-attraction',
                                        args=(self.event.id,)))
        self.assertAccessDenied(reverse('events-add-attraction',
                                        args=(self.event.id,)),
                                self.user2_data)
        self.assertAccessAllowed(reverse('events-add-attraction',
                                         args=(self.event.id,)),
                                 self.user1_data)

    def test_attraction_details_view(self):
        """
        All users should be able to see the attraction.
        """
        self.assertAccessAllowed(reverse('events-attraction-details',
                                         args=(self.attraction.id,)))
        self.assertAccessAllowed(reverse('events-attraction-details',
                                         args=(self.attraction.id,)),
                                 self.user2_data)
        self.assertAccessAllowed(reverse('events-attraction-details',
                                         args=(self.attraction.id,)),
                                 self.user1_data)

    def test_edit_attraction_view(self):
        """
        Only event owner can edit attractions.
        """

        self.assertAccessDenied(reverse('events-edit-attraction',
                                        args=(self.event.id,
                                              self.attraction.id,)))
        self.assertAccessDenied(reverse('events-edit-attraction',
                                        args=(self.event.id,
                                              self.attraction.id,)),
                                self.user2_data)
        self.assertAccessAllowed(reverse('events-edit-attraction',
                                         args=(self.event.id,
                                               self.attraction.id,)),
                                 self.user1_data)

    def test_delete_attraction_view(self):
        """
        Only event owner can delete attractions.
        """

        self.assertAccessDenied(reverse('events-delete-attraction',
                                        args=(self.event.id,
                                              self.attraction.id,)))
        self.assertAccessDenied(reverse('events-delete-attraction',
                                        args=(self.event.id,
                                              self.attraction.id,)),
                                self.user2_data)
        self.assertPOSTAccessAllowed(reverse('events-delete-attraction',
                                             args=(self.event.id,
                                                   self.attraction.id,)),
                                     self.user1_data)
