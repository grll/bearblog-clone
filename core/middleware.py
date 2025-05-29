from .models import PageView, Post


class AnalyticsMiddleware:
    """Middleware to track page views for analytics."""

    def __init__(self, get_response):
        self.get_response = get_response
        # Paths to exclude from tracking
        self.exclude_paths = [
            "/admin/",
            "/static/",
            "/media/",
            "/favicon.ico",
            "/__debug__/",
        ]

    def __call__(self, request):
        response = self.get_response(request)

        # Only track successful GET requests
        if request.method == "GET" and response.status_code == 200:
            # Check if path should be tracked
            path = request.path
            should_track = True

            for exclude in self.exclude_paths:
                if path.startswith(exclude):
                    should_track = False
                    break

            if should_track and not request.user.is_staff:
                # Track the page view
                self.track_page_view(request)

        return response

    def track_page_view(self, request):
        """Track a single page view."""
        try:
            # Get visitor info
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            referrer = request.META.get("HTTP_REFERER", "")
            session_key = request.session.session_key or ""

            # Try to associate with a post
            post = None
            if hasattr(request, "resolver_match") and request.resolver_match:
                if request.resolver_match.url_name == "post_detail":
                    slug = request.resolver_match.kwargs.get("slug")
                    if slug:
                        try:
                            post = Post.objects.get(slug=slug, published=True)
                        except Post.DoesNotExist:
                            pass

            # Create page view record
            PageView.objects.create(
                post=post,
                path=request.path,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
                session_key=session_key,
            )
        except Exception:
            # Don't let analytics errors break the site
            pass

    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
