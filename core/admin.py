from django.contrib import admin
from .models import Blog, Post


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "subdomain", "owner", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["title", "subdomain", "owner__username"]
    prepopulated_fields = {"subdomain": ("title",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "blog", "published", "published_date", "created_at"]
    list_filter = ["published", "created_at", "blog"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("blog", "title", "slug", "content")}),
        ("Publishing", {"fields": ("published", "published_date")}),
    )
