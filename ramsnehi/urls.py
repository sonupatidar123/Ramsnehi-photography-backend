from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView

def home(request):
    return HttpResponse("Backend Live ✅")

urlpatterns = [
    path('', home),  # ✅ ROOT FIX
    path('admin/', admin.site.urls),  # ✅ normal admin route
    path('ramsnehi_admin/', admin.site.urls),  # optional
    path('api/', include('gallery.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
