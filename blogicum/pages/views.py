"""Views for static project pages."""

from django.shortcuts import render


def about(request):
    """Render the project information page."""
    return render(request, 'pages/about.html')


def rules(request):
    """Render the project rules page."""
    return render(request, 'pages/rules.html')


def page_not_found(request, exception):
    """Render the custom 404 page."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Render the custom CSRF failure page."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Render the custom 500 page."""
    return render(request, 'pages/500.html', status=500)
