"""Views for displaying blog publications and user profiles."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView

from blog.forms import CommentForm, PostForm
from blog.models import Category, Comment, Post


User = get_user_model()
POSTS_PER_PAGE = 10


def filtering_posts():
    """Filter posts based on publication date and status."""
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).annotate(
        comment_count=Count('comments'),
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
    """Display a publication according to access permissions."""
    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'category',
            'location',
        ),
        pk=post_id,
    )

    if request.user != post.author:
        post = get_object_or_404(
            filtering_posts(),
            pk=post_id,
        )

    comments = post.comments.select_related('author').order_by('created_at')

    context = {
        'post': post,
        'form': CommentForm(),
        'comments': comments,
    }

    return render(request, 'blog/detail.html', context)


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
        ).annotate(
            comment_count=Count('comments'),
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


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new publication."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    login_url = 'login'

    def form_valid(self, form):
        """Assign the current user as the publication author."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the author's profile after creation."""
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    "Edit an existing post"

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post = self.get_object()
            if post.author != request.user:
                return redirect(
                    'blog:post_detail',
                    post_id=post.pk,
                )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):

        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk},
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create comment"""

    form_class = CommentForm
    template_name = 'blog/detail.html'
    login_url = 'login'

    def get_post(self):
        post = get_object_or_404(
            Post.objects.select_related('author', 'category'),
            pk=self.kwargs['post_id'],
        )

        if self.request.user != post.author:
            post = get_object_or_404(
                filtering_posts(),
                pk=post.pk,
            )

        return post

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_post()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_post()
        context['post'] = post
        context['comments'] = post.comments.select_related(
            'author'
        ).order_by('created_at')

        return context

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post_id},
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView):

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    login_url = 'login'

    def get_queryset(self):
        return super().get_queryset().filter(
            post_id=self.kwargs['post_id'],
        )

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment = self.get_object()
            if comment.author != request.user:
                return redirect(
                    'blog:post_detail',
                    post_id=comment.post_id,
                )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post_id},
        )
