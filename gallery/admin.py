from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryItem, Film, Testimonial, Inquiry


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'image_preview', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'category']
    ordering = ['-created_at']
    readonly_fields = ['image_preview', 'created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px; width:80px; object-fit:cover; border-radius:4px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    # Admin panel ki list mein ye cheezein dikhengi
    list_display = ('title', 'type', 'show_thumbnail', 'created_at')
    
    # Form mein sirf title, type aur video_id dikhega
    fields = ('title', 'type', 'video_id', 'preview_image')
    readonly_fields = ('preview_image',)

    def show_thumbnail(self, obj):
        return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.thumbnail_url)
    
    def preview_image(self, obj):
        if obj.video_id:
            return format_html('<img src="{}" style="width: 300px; height: auto; border-radius: 8px;" />', obj.thumbnail_url)
        return "Video ID daalein preview dekhne ke liye"

    show_thumbnail.short_description = 'Thumbnail'
    preview_image.short_description = 'Live Preview from YouTube'  
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'short_text', 'is_featured', 'client_image_preview', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['client_name', 'text']
    list_editable = ['is_featured']
    ordering = ['-is_featured', '-created_at']
    readonly_fields = ['client_image_preview', 'created_at']

    def short_text(self, obj):
        return obj.text[:80] + '…' if len(obj.text) > 80 else obj.text
    short_text.short_description = 'Testimonial'

    def client_image_preview(self, obj):
        if obj.client_image:
            return format_html(
                '<img src="{}" style="height:50px; width:50px; object-fit:cover; border-radius:50%;" />',
                obj.client_image.url
            )
        return '—'
    client_image_preview.short_description = 'Photo'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'mobile_number', 'inquiry_type', 'submitted_at']
    list_filter = ['inquiry_type', 'submitted_at']
    search_fields = ['full_name', 'email', 'mobile_number', 'inquiry_type']
    ordering = ['-submitted_at']
    readonly_fields = ['full_name', 'email', 'mobile_number', 'inquiry_type', 'submitted_at']

    def has_add_permission(self, request):
        # Inquiries come only from the public contact form
        return False

    def has_change_permission(self, request, obj=None):
        # Inquiries are read-only in admin (don't modify client submissions)
        return False