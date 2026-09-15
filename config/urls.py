from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("main/", include("note.urls", namespace="note")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
