from rest_framework import serializers
from .models import Image, AccountTier

class AccountTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTier
        fields = ['name', 'thumbnail_sizes', 'can_generate_expiring_links']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'image_file', 'upload_time']