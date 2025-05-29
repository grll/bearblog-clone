from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Post, PostImage, PageView, DailyAnalytics


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1  # Show one empty form by default for easy adding
    min_num = 0
    fields = ["image", "caption", "order"]
    ordering = ["order"]
    verbose_name = "Image"
    verbose_name_plural = "Images"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published", "published_date", "created_at"]
    list_filter = ["published", "created_at", "author"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    inlines = [PostImageInline]

    fieldsets = (
        (None, {"fields": ("author", "title", "slug", "content")}),
        ("Publishing", {"fields": ("published", "published_date")}),
    )

    class Media:
        css = {"all": ("admin/css/post_admin.css",)}
        js = ("admin/js/post_admin.js", "admin/js/post_images.js")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "preview/<int:post_id>/",
                self.admin_site.admin_view(self.preview_post),
                name="core_post_preview",
            ),
            path(
                "preview/new/",
                self.admin_site.admin_view(self.preview_new_post),
                name="core_post_preview_new",
            ),
            path(
                "upload-image/",
                self.admin_site.admin_view(self.upload_image),
                name="core_post_upload_image",
            ),
        ]
        return custom_urls + urls

    def preview_post(self, request, post_id):
        """Preview an existing post."""
        # Get the saved post
        post = get_object_or_404(Post, pk=post_id)

        if request.method == "POST":
            # Store preview data in session for existing posts
            request.session["preview_title"] = request.POST.get("title", post.title)
            request.session["preview_content"] = request.POST.get(
                "content", post.content
            )
            request.session["preview_post_id"] = str(post_id)
            request.session.save()

        # Check if we have session data for this post
        if request.session.get("preview_post_id") == str(post_id):
            # Use session data if available
            post.title = request.session.get("preview_title", post.title)
            post.content = request.session.get("preview_content", post.content)

        # Check if this is a popup
        is_popup = "_popup" in request.GET or "_popup" in request.POST
        template = (
            "admin/post_preview_popup.html" if is_popup else "admin/post_preview.html"
        )

        return render(
            request,
            template,
            {
                "post": post,
                "opts": self.model._meta,
                "is_popup": is_popup,
            },
        )

    def preview_new_post(self, request):
        """Preview a new post before saving."""
        if request.method == "POST":
            # Store preview data in session
            request.session["preview_title"] = request.POST.get("title", "Untitled")
            request.session["preview_content"] = request.POST.get("content", "")
            request.session.save()

        # Get preview data from session (works for both POST and GET)
        title = request.session.get("preview_title", "Untitled")
        content = request.session.get("preview_content", "")

        # Create a temporary post object (not saved to DB)
        post = Post(
            title=title,
            content=content,
            author=request.user,
        )

        # Check if this is a popup
        is_popup = "_popup" in request.GET or "_popup" in request.POST
        template = (
            "admin/post_preview_popup.html" if is_popup else "admin/post_preview.html"
        )

        return render(
            request,
            template,
            {
                "post": post,
                "opts": self.model._meta,
                "is_new": True,
                "is_popup": is_popup,
            },
        )

    def upload_image(self, request):
        """Upload image for preview in new posts."""
        if request.method != "POST" or not request.FILES.get("image"):
            return JsonResponse({"success": False, "error": "No image provided"})

        image_file = request.FILES["image"]

        # Generate a unique filename
        filename = f"preview_{image_file.name}"
        file_path = f"post_images/{filename}"

        # Save the file
        saved_path = default_storage.save(file_path, ContentFile(image_file.read()))

        # Return the URL
        image_url = request.build_absolute_uri(default_storage.url(saved_path))

        return JsonResponse({"success": True, "url": image_url, "filename": filename})


# Register analytics models
@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ["path", "timestamp", "ip_address", "post"]
    list_filter = ["timestamp", "post"]
    search_fields = ["path", "ip_address", "user_agent"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]
    readonly_fields = ["timestamp"]


@admin.register(DailyAnalytics)
class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ["date", "unique_visitors", "unique_reads", "total_views"]
    list_filter = ["date"]
    date_hierarchy = "date"
    ordering = ["-date"]
    readonly_fields = ["date", "unique_visitors", "unique_reads", "total_views"]
