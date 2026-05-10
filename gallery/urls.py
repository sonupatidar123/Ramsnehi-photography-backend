from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GalleryItemViewSet, FilmViewSet, TestimonialViewSet, InquiryViewSet, BlogViewSet, FeedbackViewSet

# Router helps automatically generate list/detail URLs



router = DefaultRouter()


# Registering views with correct basenames to match frontend URL patterns
router.register(r'gallery', GalleryItemViewSet, basename='gallery')
router.register(r'films', FilmViewSet, basename='films') 
router.register(r'testimonials', TestimonialViewSet, basename='testimonials')
router.register(r'inquiries', InquiryViewSet, basename='inquiries')
router.register(r'blogs', BlogViewSet)
router.register(r'feedbacks', FeedbackViewSet, basename='feedbacks')

urlpatterns = [
    # This includes all automatically generated routes at http://127.0.0.1:8000/api/
    path('', include(router.urls)),
     
]