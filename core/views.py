from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post


def homepage(request):
    """Homepage view with marketing content."""
    return render(request, "homepage.html")


def post_list(request):
    """List all published posts."""
    posts = Post.objects.filter(published=True, published_date__lte=timezone.now())
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, slug):
    """Display a single blog post."""
    post = get_object_or_404(
        Post, slug=slug, published=True, published_date__lte=timezone.now()
    )
    return render(request, "post_detail.html", {"post": post})
