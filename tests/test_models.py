from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.contrib.sites.models import Site
from django.urls import reverse

from robots.models import Rule, Url

from .utils import create_rules


class ModelsTestCase(TestCase):

    def setUp(self):
        self.current_site = 'example.com'
        self.site = Site.objects.get(domain=self.current_site)

    def test_get_rules(self):
        rules = Rule.get_rules()
        self.assertEqual(rules.count(), 0)

    @patch('robots.models.get_current_site')
    def test_get_rules_with_request(self, mock_get_current_site):
        mock_get_current_site.return_value = self.site
        request = 'fake_request'
        rules = Rule.get_rules(request)
        mock_get_current_site.assert_called_with(request)
        self.assertEqual(rules.count(), 0)

    @patch('robots.models.get_current_site')
    def test_get_rules_with_request(self, mock_get_current_site):
        create_rules(self.current_site)
        mock_get_current_site.return_value = self.site
        request = 'fake_request'
        rules = Rule.get_rules(request)
        mock_get_current_site.assert_called_with(request)
        self.assertEqual(rules.count(), 1)
