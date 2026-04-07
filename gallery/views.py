from rest_framework import viewsets, permissions, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import GalleryItem, Film, Testimonial, Inquiry
from .serializers import (
    GalleryItemSerializer, FilmSerializer, 
    TestimonialSerializer, InquirySerializer
)

class GalleryItemViewSet(viewsets.ModelViewSet):
    """
    Admin can CRUD, Public can only List/Retrieve.
    """
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'category']
    ordering = ['-created_at']

    def get_permissions(self):
        # Agar request GET hai toh sabko allow karein, 
        # Agar POST/DELETE/PUT hai toh sirf Admin.
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['title', 'type']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_featured']
    search_fields = ['client_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class InquiryViewSet(viewsets.ModelViewSet):
    """
    Public can only POST (Create), Admin can do everything.
    """
    queryset = Inquiry.objects.all().order_by('-submitted_at')
    serializer_class = InquirySerializer

    def get_permissions(self):
        # Public ko sirf inquiry bhejni (POST) ki permission hai
        if self.action == 'create':
            return [AllowAny()]
        # Baaki sab (List, Delete, Update) sirf Admin ke liye
        return [IsAdminUser()]