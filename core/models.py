from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.safestring import mark_safe
import markdown


class Post(models.Model):
    """Blog post model."""

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(help_text="You can use Markdown formatting")
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_content_as_markdown(self):
        """Convert markdown content to HTML with syntax highlighting."""
        md = markdown.Markdown(
            extensions=["extra", "codehilite", "toc"],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "use_pygments": True,
                    "guess_lang": False,
                }
            },
        )
        return mark_safe(md.convert(self.content))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_date", "-created_at"]


class PostImage(models.Model):
    """Images associated with blog posts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_images/")
    caption = models.CharField(
        max_length=200, blank=True, help_text="Optional caption for the image"
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Order of display (lower numbers first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_markdown(self):
        """Get markdown syntax for this image."""
        alt_text = self.caption or f"Image {self.order + 1}"
        return f"![{alt_text}]({self.image.url})"

    def __str__(self):
        return f"Image for {self.post.title} ({self.order})"

    class Meta:
        ordering = ["order", "created_at"]


class PageView(models.Model):
    """Track individual page views for analytics."""

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="views", null=True, blank=True
    )
    path = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referrer = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"{self.path} - {self.timestamp}"

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["post", "-timestamp"]),
            models.Index(fields=["session_key", "-timestamp"]),
        ]


class DailyAnalytics(models.Model):
    """Aggregated daily analytics data."""

    date = models.DateField(unique=True)
    unique_visitors = models.IntegerField(default=0)
    unique_reads = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)

    def __str__(self):
        return f"Analytics for {self.date}"

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Daily analytics"
