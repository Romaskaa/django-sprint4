"""Views for static project pages."""

from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Render the custom 404 page."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Render the custom CSRF failure page."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Render the custom 500 page."""
    return render(request, 'pages/500.html', status=500)
