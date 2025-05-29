import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Post


@pytest.mark.django_db
def test_post_creation():
    """Test creating a blog post."""
    user = User.objects.create_user(username="testuser", password="testpass")

    post = Post.objects.create(
        author=user,
        title="Test Post",
        content="This is test content",
        published=True,
        published_date=timezone.now(),
    )

    assert post.title == "Test Post"
    assert post.slug == "test-post"  # Should be auto-generated
    assert post.author == user
    assert str(post) == "Test Post"


@pytest.mark.django_db
def test_post_slug_generation():
    """Test that post slugs are generated from titles."""
    user = User.objects.create_user(username="testuser", password="testpass")

    post = Post.objects.create(
        author=user, title="This is a Test Post!", content="Content"
    )

    assert post.slug == "this-is-a-test-post"
