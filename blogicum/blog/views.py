"""Views for displaying blog publications and user profiles."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView

from blog.models import Category, Post


User = get_user_model()
POSTS_PER_PAGE = 10


def filtering_posts():
    """Filter posts based on publication date and status."""
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    """Render the main page."""
    posts = filtering_posts().select_related(
        'author',
        'category',
        'location',
    )
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'blog/index.html', {'page_obj': page_obj})


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

    posts = filtering_posts().filter(category=category).select_related(
        'author',
        'category',
        'location',
    )
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


class ProfileView(ListView):
    """Display a user profile and its publications."""

    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'post_list'
    paginate_by = POSTS_PER_PAGE

    def get_profile(self):
        """Return the profile owner requested in the URL."""
        if not hasattr(self, 'profile_user'):
            self.profile_user = get_object_or_404(
                User,
                username=self.kwargs['username'],
            )
        return self.profile_user

    def get_queryset(self):
        """Return all own posts to the owner and public posts to others."""
        profile_user = self.get_profile()
        posts = Post.objects.filter(author=profile_user).select_related(
            'author',
            'category',
            'location',
        )
        if self.request.user != profile_user:
            posts = posts.filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True,
            )
        return posts

    def get_context_data(self, **kwargs):
        """Add the profile owner to the template context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Allow an authenticated user to edit their own profile."""

    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """Return only the currently authenticated user."""
        return self.request.user

    def get_success_url(self):
        """Redirect to the updated profile."""
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.username},
        )
