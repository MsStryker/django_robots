from unittest.mock import patch
from django.test import Client, TestCase, override_settings
from django.contrib.sites.models import Site
from django.urls import reverse

from robots.models import Rule, Url


def create_rules(current_site):
    site_1 = Site.objects.get(domain=current_site)
    site_2 = Site.objects.create(domain='sub.example.com')

    url_check = Url.objects.create(pattern='/malware-bot-test')
    url_root = Url.objects.create(pattern='/')
    url_media = Url.objects.create(pattern='/media')

    rule_1 = Rule.objects.create(site=site_1, user_agent='*', crawl_delay=10)
    rule_2 = Rule.objects.create(site=site_2, user_agent='*', crawl_delay=10)
    rule_3 = Rule.objects.create(user_agent='Bing', crawl_delay=20)
    rule_4 = Rule.objects.create(user_agent='Googlebot')

    rule_1.allowed_urls.add(url_root)
    for url in [url_check, url_media]:
        rule_1.disallowed_urls.add(url)

    rule_2.allowed_urls.add(url_root)
    rule_3.disallowed_urls.add(url_media)
    rule_4.disallowed_urls.add(url_media)

