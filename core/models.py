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
            extensions=[
                "extra",
                "codehilite", 
                "toc"
            ],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "use_pygments": True,
                    "guess_lang": False,
                }
            }
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
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption for the image")
    order = models.PositiveIntegerField(default=0, help_text="Order of display (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_markdown(self):
        """Get markdown syntax for this image."""
        alt_text = self.caption or f"Image {self.order + 1}"
        return f"![{alt_text}]({self.image.url})"
    
    def __str__(self):
        return f"Image for {self.post.title} ({self.order})"
    
    class Meta:
        ordering = ["order", "created_at"]
