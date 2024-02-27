from django.contrib import admin

from .models import Category, Location, Post, Comment

admin.site.empty_value_display = "Не задано"


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "is_published",
        "created_at",
        "pub_date",
        "author",
        "location",
        "category",
    )
    list_editable = ("is_published", "category")
    search_fields = ("title",)
    list_filter = ("category",)
    list_display_links = ("title",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        "title",
        "description",
        "slug",
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name","text","created_at","post")