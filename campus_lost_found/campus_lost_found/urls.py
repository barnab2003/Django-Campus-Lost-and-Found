# campus_lost_found/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # <-- ADD THIS
from django.conf.urls.static import static   # <-- ADD THIS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', include('items.urls')),
]

# --- ADD THIS BLOCK ---
# This allows Django to serve uploaded images during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)