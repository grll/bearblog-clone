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
