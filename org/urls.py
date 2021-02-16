
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls.conf import include

urlpatterns = [
    path('auth/', include('users.urls')),
    path('post/', include('posts.urls')),
    path('follow/', include('follows.urls')),
    path('content/', include('contents.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
