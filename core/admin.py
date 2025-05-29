from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published", "published_date", "created_at"]
    list_filter = ["published", "created_at", "author"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("author", "title", "slug", "content")}),
        ("Publishing", {"fields": ("published", "published_date")}),
    )

    class Media:
        css = {"all": ("admin/css/post_admin.css",)}
        js = ("admin/js/post_admin.js",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "preview/<int:post_id>/",
                self.admin_site.admin_view(self.preview_post),
                name="core_post_preview",
            ),
        ]
        return custom_urls + urls

    def preview_post(self, request, post_id):
        """Preview a post before publishing."""
        post = get_object_or_404(Post, pk=post_id)
        return render(
            request,
            "admin/post_preview.html",
            {
                "post": post,
                "opts": self.model._meta,
            },
        )
