from django.contrib import admin
from .models import Teaching, Media, Event, CommunityPost


@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'views', 'is_published', 'created_at')
    list_filter = ('media_type', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'location', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'location')


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'email')

def save_model(self, request, obj, form, change):
    if obj.media_type == 'video' and not obj.video_file:
        raise ValueError("Video must have a video file")
    super().save_model(request, obj, form, change)