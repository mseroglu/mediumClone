from django.contrib import admin
from .models import Tag, Category, BlogPost, UserPostFav


@admin.register(UserPostFav)
class AdminTag(admin.ModelAdmin):
    list_display = ["user", "post", "is_deleted"]


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ["title", "slug", "is_active"]


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ["title", "slug", "is_active"]


@admin.register(BlogPost)
class AdminPost(admin.ModelAdmin):
    list_display = ["title", "slug", "view_count", "is_active"]
