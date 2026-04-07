from rest_framework import serializers
from .models import GalleryItem, Film, Testimonial, Inquiry

# ---------------------------------------------------------------------------
# 1. GALLERY SERIALIZER
# ---------------------------------------------------------------------------
class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = ['id', 'title', 'image', 'category', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        return representation


# ---------------------------------------------------------------------------
# 2. FILM SERIALIZER
# ---------------------------------------------------------------------------
class FilmSerializer(serializers.ModelSerializer):
    # We include the thumbnail_url property from our Model
    thumbnail_url = serializers.ReadOnlyField()

    class Meta:
        model = Film
        fields = ['id', 'title', 'type', 'video_id', 'thumbnail_url', 'created_at']


# ---------------------------------------------------------------------------
# 3. TESTIMONIAL SERIALIZER
# ---------------------------------------------------------------------------
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'text', 'client_image', 
            'is_featured', 'created_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.client_image:
            representation['client_image'] = instance.client_image.url
        return representation


# ---------------------------------------------------------------------------
# 4. INQUIRY SERIALIZER
# ---------------------------------------------------------------------------
class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = [
            'id', 'full_name', 'email', 'mobile_number', 
            'inquiry_type', 'submitted_at'
        ]
        read_only_fields = ['submitted_at']