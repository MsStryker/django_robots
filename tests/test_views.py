from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.contrib.sites.models import Site
from django.urls import reverse

from robots.models import Rule, Url

from .utils import create_rules


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.current_site = 'example.com'
        self.sub_site = 'sub.example.com'
        self.robot_url = reverse('robots')
        self.generic_user_agent = 'User-agent: *'
        self.generic_disallow_empty = 'Disallow:\n'
        self.malware_str = 'Disallow: /malware-bot-test'

    def assert_contains(self, test_str, content_str):
        if isinstance(content_str, bytes):
            content_str = content_str.decode('utf-8')

        self.assertIn(test_str, content_str)

    def assert_does_not_contain(self, test_str, content_str):
        if isinstance(content_str, bytes):
            content_str = content_str.decode('utf-8')

        self.assertNotIn(test_str, content_str)

    def test_view(self):
        create_rules(self.current_site)
        response = self.client.get(self.robot_url, secure=False, SERVER_NAME=self.current_site)
        self.assertEqual(response.status_code, 200)
        self.assert_contains(self.generic_user_agent, response.content)
        self.assert_does_not_contain(self.generic_disallow_empty, response.content)
        self.assert_contains(self.malware_str, response.content)

    def test_view_secure(self):
        create_rules(self.current_site)
        response = self.client.get(self.robot_url, secure=True, SERVER_NAME=self.current_site)
        self.assertEqual(response.status_code, 200)
        self.assert_contains(self.generic_user_agent, response.content)
        self.assert_does_not_contain(self.generic_disallow_empty, response.content)
        self.assert_contains(self.malware_str, response.content)

    def test_view_sub_view(self):
        create_rules(self.current_site)
        response = self.client.get(self.robot_url, secure=True, SERVER_NAME=self.sub_site)
        self.assertEqual(response.status_code, 200)
        self.assert_contains(self.generic_user_agent, response.content)
        self.assert_does_not_contain(self.generic_disallow_empty, response.content)
        self.assert_contains(self.malware_str, response.content)

    @override_settings(USES_HTTP=True)
    def test_view_http(self):
        response = self.client.get(self.robot_url, SERVER_NAME=self.current_site)
        self.assertEqual(response.status_code, 200)
        self.assert_contains(self.generic_user_agent, response.content)
        self.assert_contains(self.generic_disallow_empty, response.content)
        self.assert_does_not_contain(self.malware_str, response.content)

    @override_settings(USES_HTTPS=True)
    def test_view_https(self):
        response = self.client.get(self.robot_url, SERVER_NAME=self.current_site)
        self.assertEqual(response.status_code, 200)
        self.assert_contains(self.generic_user_agent, response.content)
        self.assert_contains(self.generic_disallow_empty, response.content)
        self.assert_does_not_contain(self.malware_str, response.content)
