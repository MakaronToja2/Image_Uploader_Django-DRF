from django.urls import path, include
from django.contrib import admin
from image_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list_images/', views.ListImageViewSet.as_view({'get': 'list'}), name='list-images'),
    path('add_image/', views.AddImageViewSet.as_view({'post': 'create'}), name='add-image'),
    path('images/<int:pk>/', views.ImageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='image-detail'),
    path('images/<int:pk>/thumbnail_<str:thumbnail_size>_<str:image_name>/', views.serve_image, name='serve-image'),
    path('original_<path:image_name>/', views.serve_original_image, name='serve-original-image'),
    path('expiring_original_<path:image_name>/', views.serve_expiring_image, name='serve-expiring-image'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)