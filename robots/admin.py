from django.contrib import admin
from django.contrib.admin import register
from django.utils.translation import ugettext_lazy as _

from robots.forms import RuleAdminForm
from robots.models import Rule, Url


@register(Rule)
class RuleAdmin(admin.ModelAdmin):
    form = RuleAdminForm
    fieldsets = (
        (None, {'fields': ('user_agent', 'site', 'comment')}),
        (_('URL patterns'), {
            'fields': ('allowed_urls', 'disallowed_urls'),
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('crawl_delay',),
        }),
    )
    list_filter = ('site',)
    list_display = ('site', 'user_agent', 'allowed', 'disallowed')
    search_fields = ('user_agent', 'allowed__pattern', 'disallowed__pattern')
    filter_horizontal = ('allowed_urls', 'disallowed_urls')
    save_as = True


admin.site.register(Url)
