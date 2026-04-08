from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
<<<<<<< HEAD
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ added TokenRefreshView

def home(request):
    return HttpResponse("Backend Live ✅")
=======
from rest_framework_simplejwt.views import TokenObtainPairView
>>>>>>> d30e85ae0f62112da6cb9fcfd1fe6e7eb93984c1

def home(request):
    return HttpResponse("Backend Live ✅")

urlpatterns = [
<<<<<<< HEAD
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('gallery.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ THIS WAS MISSING
]
=======
    path('', home),  # ✅ ROOT FIX
    path('admin/', admin.site.urls),  # ✅ normal admin route
    path('ramsnehi_admin/', admin.site.urls),  # optional
    path('api/', include('gallery.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
>>>>>>> d30e85ae0f62112da6cb9fcfd1fe6e7eb93984c1
