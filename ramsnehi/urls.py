from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ added TokenRefreshView

def home(request):
    return HttpResponse("Backend Live ✅")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('gallery.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ THIS WAS MISSING
]