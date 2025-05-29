import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_loads():
    """Test that the homepage loads successfully."""
    client = Client()
    response = client.get(reverse("homepage"))

    assert response.status_code == 200
    assert b"Bear" in response.content
    assert b"privacy-first" in response.content


@pytest.mark.django_db
def test_homepage_content():
    """Test that the homepage contains all required marketing content."""
    client = Client()
    response = client.get(reverse("homepage"))
    content = response.content.decode("utf-8")

    # Test main headings
    assert "ʕ•ᴥ•ʔ Bear" in content
    assert "A privacy-first, no-nonsense, super-fast blogging platform" in content
    assert "No trackers, no javascript, no stylesheets. Just your words." in content

    # Test navigation buttons (using Django admin)
    assert "Log in" in content
    assert "Blog" in content

    # Test value proposition
    assert "This is a blogging platform where words matter most." in content
    assert "necessities" in content

    # Test feature list (checking key parts due to HTML tags)
    assert "Looks great on" in content
    assert "device" in content
    assert "Tiny (~2.7kb), optimized, and awesome pages" in content
    assert "No trackers, ads, or scripts" in content
    assert "Seconds to" in content
    assert "Connect your custom domain" in content
    assert "Free themes" in content
    assert "RSS & Atom feeds" in content
    assert "Built to last forever" in content

    # Test links
    assert "View example blog" in content
    assert "https://herman.bearblog.dev" in content

    # Test CTA
    assert "Publish something awesome with your" in content
    assert "hands" in content
    assert "ᕦʕ •ᴥ•ʔᕤ" in content

    # Test footer
    assert "Privacy Policy" in content
    assert "Terms of Service" in content
    assert "GitHub" in content
    assert "Docs" in content
    assert "Roadmap" in content
