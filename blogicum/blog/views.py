"""Views for displaying blog publications."""

from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post


def filtering_posts():
    """Filter posts based on publication date and status."""
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    """Render the main page."""
    posts = filtering_posts()[:5]

    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    """Render a publication page placeholder."""
    post = get_object_or_404(
        filtering_posts(),
        pk=post_id,
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Render a category page placeholder."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    posts = filtering_posts().filter(category=category)

    context = {'category': category, 'post_list': posts}
    return render(request, 'blog/category.html', context)
