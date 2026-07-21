from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin
admin.site.site_header = 'ConnectHub Administration'
admin.site.site_title = 'ConnectHub Admin'
admin.site.index_title = 'Welcome to ConnectHub Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace='posts')),
    path('users/', include('users.urls', namespace='users')),
    # REST API endpoints
    path('api/', include('posts.api_urls')),
    path('api/users/', include('users.api_urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)