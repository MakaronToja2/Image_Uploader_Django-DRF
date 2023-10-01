from rest_framework import viewsets, generics
from .models import Image, CustomUser
from .serializers import BasicImageSerializer, PremiumImageSerializer, EnterpriseImageSerializer, WriteImageSerializer


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



