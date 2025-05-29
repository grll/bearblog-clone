from django.conf import settings


def blog_settings(request):
    """Add blog settings to template context."""
    return {
        "BLOG_TITLE": settings.BLOG_TITLE,
        "BLOG_DESCRIPTION": settings.BLOG_DESCRIPTION,
        "BLOG_FOOTER_LINKS": settings.BLOG_FOOTER_LINKS,
    }
