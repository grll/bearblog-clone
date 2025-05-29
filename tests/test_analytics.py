import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import PageView, DailyAnalytics, Post
from datetime import timedelta


class AnalyticsMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass"
        )
        self.post = Post.objects.create(
            author=self.admin,
            title="Test Post",
            slug="test-post",
            content="Test content",
            published=True,
            published_date=timezone.now(),
        )

    def test_anonymous_user_views_are_tracked(self):
        """Test that anonymous user page views are tracked."""
        initial_count = PageView.objects.count()

        # Visit homepage
        response = self.client.get("/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)

        # Visit blog post
        response = self.client.get(f"/blog/{self.post.slug}/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)

        # Check that views were recorded
        new_count = PageView.objects.count()
        self.assertEqual(new_count - initial_count, 2)

        # Check that post association works
        post_view = PageView.objects.filter(post=self.post).first()
        self.assertIsNotNone(post_view)
        self.assertEqual(post_view.path, f"/blog/{self.post.slug}/")

    def test_staff_user_views_not_tracked(self):
        """Test that staff user views are not tracked."""
        self.client.force_login(self.admin)
        initial_count = PageView.objects.count()

        # Visit pages as admin
        response = self.client.get("/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/blog/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)

        # Check that no views were recorded
        new_count = PageView.objects.count()
        self.assertEqual(new_count, initial_count)

    def test_admin_paths_not_tracked(self):
        """Test that admin paths are not tracked."""
        initial_count = PageView.objects.count()

        # Visit admin page
        response = self.client.get("/admin/", HTTP_HOST="localhost")
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

        # Check that no view was recorded
        new_count = PageView.objects.count()
        self.assertEqual(new_count, initial_count)

    def test_daily_analytics_aggregation(self):
        """Test daily analytics aggregation."""
        # Create some analytics data directly
        today = timezone.now().date()
        
        analytics = DailyAnalytics.objects.create(
            date=today,
            unique_visitors=100,
            unique_reads=50,
            total_views=200
        )

        # Check the data
        self.assertEqual(analytics.unique_visitors, 100)
        self.assertEqual(analytics.unique_reads, 50)
        self.assertEqual(analytics.total_views, 200)


class AnalyticsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass"
        )

    def test_analytics_dashboard_requires_staff(self):
        """Test that analytics dashboard requires staff access."""
        # Try without login
        response = self.client.get("/admin/analytics/")
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Try with non-staff user
        user = User.objects.create_user(username="user", password="pass")
        self.client.force_login(user)
        response = self.client.get("/admin/analytics/")
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Try with staff user
        self.client.force_login(self.admin)
        response = self.client.get("/admin/analytics/")
        self.assertEqual(response.status_code, 200)

    def test_analytics_dashboard_context(self):
        """Test analytics dashboard context data."""
        self.client.force_login(self.admin)

        # Create some analytics data
        today = timezone.now().date()
        DailyAnalytics.objects.create(
            date=today, unique_visitors=100, unique_reads=50, total_views=200
        )

        response = self.client.get("/admin/analytics/")
        self.assertEqual(response.status_code, 200)

        # Check context
        self.assertIn("unique_visitors", response.context)
        self.assertIn("unique_reads", response.context)
        self.assertIn("chart_svg", response.context)
        self.assertIn("daily_data", response.context)