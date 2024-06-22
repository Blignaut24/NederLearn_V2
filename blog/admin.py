# ---------------------
# Django Imports
# ---------------------
from django.contrib import admin
from .models import Blogpost, Comment ,MediaCategory
from django_summernote.admin import SummernoteModelAdmin

# ---------------------
# Register your models
# ---------------------

@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    # Define display fields
    list_display = ('media_name',)
    # Define search fields
    search_fields = ('media_name',)

@admin.register(Blogpost)
class PostAdmin(SummernoteModelAdmin):
    # Each blogpost display features are defined here
    list_display = ('blog_title', 'slug', 'status', 'created_on')
    # Define search fields
    search_fields = ('blog_title', 'content')
    # Define prepopulated fields
    prepopulated_fields = {'slug': ('blog_title',)}
    # Define filter fields
    list_filter = ('status', 'created_on')
    # Define summernote fields
    summernote_fields = ('content')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Define display fields for the user's profile
    list_display = ('user', 'bio', 'country')
    # Define search fields
    search_fields = ('user__username', 'bio')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Define display fields for comments
    list_display = ('user', 'body', 'post', 'created_on', 'approved')
    # Define filter fields
    list_filter = ('approved', 'created_on')
    # Define search fields
    search_fields = ('user', 'body', 'post')
    # Define actions
    actions = ['approved_comments']

    # Define approved comments function
    def approved_comments(self, request, queryset):
        queryset.update(approved=True)
