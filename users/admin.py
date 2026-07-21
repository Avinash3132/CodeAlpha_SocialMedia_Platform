from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = [
        'bio', 'profile_picture',
        'website', 'location'
    ]


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = [
        'username', 'email', 'first_name',
        'last_name', 'is_staff', 'avatar'
    ]

    def avatar(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return format_html(
                '<img src="{}" width="35" height="35" '
                'style="border-radius:50%; object-fit:cover;" />',
                obj.profile.profile_picture.url
            )
        return mark_safe(
            '<div style="width:35px;height:35px;background:#6366f1;'
            'border-radius:50%;display:flex;align-items:center;'
            'justify-content:center;color:white;font-weight:700;">'
            '</div>'
        )
    avatar.short_description = 'Avatar'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'followers_count', 'following_count']
    search_fields = ['user__username', 'user__email']

    def followers_count(self, obj):
        return obj.get_followers_count()
    followers_count.short_description = 'Followers'

    def following_count(self, obj):
        return obj.get_following_count()
    following_count.short_description = 'Following'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)