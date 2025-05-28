import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Blog, Post


@pytest.mark.django_db
def test_blog_creation():
    """Test creating a blog."""
    user = User.objects.create_user(username="testuser", password="testpass")
    blog = Blog.objects.create(
        owner=user, title="Test Blog", subdomain="test-blog", description="A test blog"
    )

    assert blog.title == "Test Blog"
    assert blog.subdomain == "test-blog"
    assert blog.owner == user
    assert str(blog) == "Test Blog"


@pytest.mark.django_db
def test_post_creation():
    """Test creating a blog post."""
    user = User.objects.create_user(username="testuser", password="testpass")
    blog = Blog.objects.create(owner=user, title="Test Blog", subdomain="test-blog")

    post = Post.objects.create(
        blog=blog,
        title="Test Post",
        content="This is test content",
        published=True,
        published_date=timezone.now(),
    )

    assert post.title == "Test Post"
    assert post.slug == "test-post"  # Should be auto-generated
    assert post.blog == blog
    assert str(post) == "Test Post"


@pytest.mark.django_db
def test_post_slug_generation():
    """Test that post slugs are generated from titles."""
    user = User.objects.create_user(username="testuser", password="testpass")
    blog = Blog.objects.create(owner=user, title="Test Blog", subdomain="test")

    post = Post.objects.create(
        blog=blog, title="This is a Test Post!", content="Content"
    )

    assert post.slug == "this-is-a-test-post"
