from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['user', 'content', 'created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'short_content',
        'likes_count', 'comments_count',
        'has_image', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    inlines = [CommentInline]
    date_hierarchy = 'created_at'

    def short_content(self, obj):
        text = obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
        return text or '— no text —'
    short_content.short_description = 'Content'

    def likes_count(self, obj):
        return obj.get_likes_count()
    likes_count.short_description = 'Likes'

    def comments_count(self, obj):
        return obj.get_comments_count()
    comments_count.short_description = 'Comments'

    def has_image(self, obj):
        if obj.image:
            return mark_safe(
                '<span style="color:#059669; font-weight:700;">Yes</span>'
            )
        return mark_safe(
            '<span style="color:#94a3b8;">No</span>'
        )
    has_image.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" '
                'style="border-radius:8px; object-fit:cover;"/>',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Preview'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']