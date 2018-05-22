from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Url(models.Model):
    """
    Defines a URL pattern for use with a robot exclusion rule. It's
    case-sensitive and exact, e.g., "/admin" and "/admin/" are different URLs.
    """
    pattern = models.CharField(
        _('pattern'),
        max_length=255,
        help_text=_("Case-sensitive. A missing trailing slash does also match to files "
                    "which start with the name of the pattern, e.g., '/admin' matches "
                    "/admin.html too. Some major search engines allow an asterisk (*) "
                    "as a wildcard and a dollar sign ($) to match the end of the URL, "
                    "e.g., '/*.jpg$'."))

    class Meta:
        verbose_name = _('url')
        verbose_name_plural = _('url')

    def __str__(self):
        return self.pattern

    def save(self, *args, **kwargs):
        if not self.pattern.startswith('/'):
            self.pattern = '/' + self.pattern
        super(Url, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Rule(models.Model):
    """
    Defines an abstract rule which is used to respond to crawling web robots,
    using the robot exclusion standard, a.k.a. robots.txt. It allows or
    disallows the robot identified by its user agent to access the given URLs.
    The Site contrib app is used to enable multiple robots.txt per instance.
    """
    site = models.ForeignKey(Site, verbose_name=_('sites'), blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.CharField(
        _('User-agent'),
        default='*',
        max_length=255,
        help_text=_("This should be a user agent string like 'Googlebot'. Enter an "
                    "asterisk (*) for all user agents. For a full list look at the "
                    "<a target=_blank href='http://www.robotstxt.org/db.html'> "
                    "database of Web Robots</a>."))

    allowed_urls = models.ManyToManyField(
        Url,
        blank=True,
        related_name="allowed_urls",
        verbose_name=_('Allowed'),
        help_text=_("The URLs which are allowed to be accessed by bots."))

    disallowed_urls = models.ManyToManyField(
        Url,
        blank=True,
        related_name="disallowed_urls",
        verbose_name=_('Disallowed'),
        help_text=_("The URLs which are not allowed to be accessed by bots. Do not "
                    "put hidden URLs, as malicious bots with look at these!"))

    crawl_delay = models.DecimalField(
        _('Crawl-delay'),
        blank=True, null=True,
        max_digits=3,
        decimal_places=1,
        help_text=_("Between 0.1 and 99.0. This field is supported by some search "
                    "engines and defines the delay between successive crawler "
                    "accesses in seconds. If the crawler rate is a problem for your "
                    "server, you can set the delay up to 5 or 10 or a comfortable "
                    "value for your server, but it's suggested to start with small "
                    "values (0.5-1), and increase as needed to an acceptable value "
                    "for your server. Larger delay values add more delay between "
                    "successive crawl accesses and decrease the maximum crawl rate to "
                    "your web server."))

    class Meta:
        verbose_name = _('Rule')
        verbose_name_plural = _('Rules')
        unique_together = (('user_agent', 'site'),)

    def __str__(self):
        return self.user_agent

    @property
    def allowed(self):
        objs = self.allowed_urls.values_list('pattern', flat=True)
        return mark_safe('<br>'.join(objs))

    @property
    def disallowed(self):
        objs = self.disallowed_urls.values_list('pattern', flat=True)
        return mark_safe('<br>'.join(objs))

    @classmethod
    def get_rules(cls, request=None):
        if request:
            site = get_current_site(request)
            return cls.objects.filter(site__id=site.id)
        return cls.objects.filter(site__isnull=True)
