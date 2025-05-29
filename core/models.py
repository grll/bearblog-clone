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
        """Convert markdown content to HTML."""
        md = markdown.Markdown(extensions=["extra", "codehilite", "toc"])
        return mark_safe(md.convert(self.content))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_date", "-created_at"]
