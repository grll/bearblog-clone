from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Blog, Post


def homepage(request):
    """Homepage view with marketing content."""
    return render(request, "homepage.html")


def blog_list(request):
    """List all blogs with published posts."""
    blogs = Blog.objects.filter(posts__published=True).distinct()
    return render(request, "blog_list.html", {"blogs": blogs})


def blog_detail(request, subdomain):
    """Display a blog's homepage with recent posts."""
    blog = get_object_or_404(Blog, subdomain=subdomain)
    posts = blog.posts.filter(published=True, published_date__lte=timezone.now())
    return render(request, "blog_detail.html", {"blog": blog, "posts": posts})


def post_detail(request, subdomain, slug):
    """Display a single blog post."""
    blog = get_object_or_404(Blog, subdomain=subdomain)
    post = get_object_or_404(
        Post, blog=blog, slug=slug, published=True, published_date__lte=timezone.now()
    )
    return render(request, "post_detail.html", {"blog": blog, "post": post})
