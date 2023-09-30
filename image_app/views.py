from rest_framework import viewsets
from .models import Image, AccountTier
from .serializers import ImageSerializer, AccountTierSerializer

class AccountTierViewSet(viewsets.ModelViewSet):
    queryset = AccountTier.objects.all()
    serializer_class = AccountTierSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer