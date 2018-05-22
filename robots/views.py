from django.views.generic import ListView

from robots.models import Rule


class RobotsListView(ListView):
    """
    Returns a generated robots.txt file.
    """
    model = Rule
    context_object_name = 'rules'
    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_queryset(self):
        return self.model.get_rules(self.request)
