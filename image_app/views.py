from rest_framework import viewsets
from .models import Image, CustomUser
from .serializers import BasicImageSerializer, PremiumImageSerializer, EnterpriseImageSerializer, WriteImageSerializer
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
import os
from django.conf import settings


from rest_framework import viewsets

class AddImageViewSet(viewsets.ModelViewSet):
    serializer_class = WriteImageSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        user = self.request.user
        if user.account_tier == CustomUser.BASIC:
            return BasicImageSerializer
        elif user.account_tier == CustomUser.PREMIUM:
            return PremiumImageSerializer
        elif user.account_tier == CustomUser.ENTERPRISE:
            return EnterpriseImageSerializer
        else:
            return BasicImageSerializer  # Default, can also raise an exception if needed

class ListImageViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        user = self.request.user
        if user.account_tier == CustomUser.BASIC:
            return BasicImageSerializer
        elif user.account_tier == CustomUser.PREMIUM:
            return PremiumImageSerializer
        elif user.account_tier == CustomUser.ENTERPRISE:

            return EnterpriseImageSerializer
        else:
            return BasicImageSerializer  # Default, can also raise an exception if needed

def serve_image(request, pk, thumbnail_size, image_name):
    image = get_object_or_404(Image, pk=pk)
    print(f"PK: {pk}, Thumbnail Size: {thumbnail_size}, Image Name: {image_name}")
    # Constructing the full image name
    full_image_name = f"thumbnail_{thumbnail_size}_{image_name}"

    # Constructing the image path
    image_path = os.path.join(settings.MEDIA_ROOT, full_image_name)

    print(f"Checking if image exists at {image_path}")

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            # Determine content type dynamically
            content_type = 'image/jpeg' if '.jpg' in full_image_name else 'image/png'
            return HttpResponse(f, content_type=content_type)
    else:
        raise Http404("Image does not exist")

def serve_original_image(request, image_name):
    # Using Django's settings to get the media root directory
    image_directory = settings.MEDIA_ROOT

    # Constructing the full image path
    absolute_path = os.path.join(image_directory, image_name)
    print(absolute_path)

    if os.path.exists(absolute_path):
        with open(absolute_path, 'rb') as f:
            # Determine content type dynamically
            content_type = 'image/jpeg' if '.jpg' in image_name else 'image/png'
            return HttpResponse(f, content_type=content_type)
    else:
        raise Http404("Image does not exist")

def serve_expiring_image(request, image_name):
    """Serves an expiring image."""
    # Construct the full path to the image.
    expiring_image_path = os.path.join(settings.MEDIA_ROOT, 'expiring_images', image_name)
    print(f"Expected expiring_image_path in serve_expiring_image: {expiring_image_path}")
    # Check if the image exists and then serve it
    if os.path.exists(expiring_image_path):
        with open(expiring_image_path, 'rb') as f:
            print(f"Serving image from path: {expiring_image_path}")
            return HttpResponse(f, content_type='image/jpeg')
    else:
        # Handle file not found case.
        print(f"File not found at path: {expiring_image_path}")
        return Http404("Image not found")
