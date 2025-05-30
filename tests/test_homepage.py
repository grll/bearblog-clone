import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_loads():
    """Test that the homepage loads successfully."""
    client = Client()
    response = client.get(reverse("homepage"))

    assert response.status_code == 200
    assert b"Guillaume Raille" in response.content  # Blog title from settings
    assert b"data scientist" in response.content  # Part of blog description


@pytest.mark.django_db
def test_homepage_navigation():
    """Test that the homepage has proper navigation."""
    client = Client()
    response = client.get(reverse("homepage"))
    content = response.content.decode("utf-8")

    # Test navigation
    assert "Home" in content
    assert "Blog" in content

    # Test footer
    assert "Made with" in content
    assert "Bear ʕ•ᴥ•ʔ" in content
