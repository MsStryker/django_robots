from django import forms
from django.utils.translation import ugettext_lazy as _

from robots.models import Rule


class RuleAdminForm(forms.ModelForm):
    URL_MISSING_ERROR = _('Please specify at least one allowed or dissallowed URL.')
    URL_REPEAT_ERROR = _('Allowed and Disallowed URLs must be different.')

    class Meta:
        model = Rule
        fields = "__all__"

    def data_count(self, data):
        if not data:
            return 0
        return data.count()

    def clean(self):
        cleaned_data = super(RuleAdminForm, self).clean()
        allowed_data = cleaned_data.get('allowed_urls')
        disallowed_data = cleaned_data.get('disallowed_urls')
        total_allowed = self.data_count(allowed_data)
        total_disallowed = self.data_count(disallowed_data)
        total_urls = total_allowed + total_disallowed
        if total_urls == 0:
            self.add_error('allowed_urls', self.URL_MISSING_ERROR)
            self.add_error('disallowed_urls', self.URL_MISSING_ERROR)

        if (allowed_data | disallowed_data).count() != total_urls:
            self.add_error('allowed_urls', self.URL_REPEAT_ERROR)
            self.add_error('disallowed_urls', self.URL_REPEAT_ERROR)

        return cleaned_data
