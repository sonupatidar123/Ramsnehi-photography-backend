from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('ramsnehi_admin/', admin.site.urls),
    path('api/', include('gallery.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
