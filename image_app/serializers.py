from rest_framework import serializers
from .models import Image, CustomUser
from django.urls import reverse

class WriteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image_file', 'upload_time']

class BaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'upload_time']


    def get_thumbnail_urls(self, obj):
        user = self.context['request'].user
        thumbnails = {}

        base_url = self.context['request'].build_absolute_uri(reverse('image-detail', args=[obj.id]))

        if user.account_tier == CustomUser.BASIC:
            thumbnails['thumbnail_200'] = f"{base_url}thumbnail_200_{obj.image_file.name.split('/')[-1]}"
        elif user.account_tier == CustomUser.PREMIUM:
            thumbnails['thumbnail_200'] = f"{base_url}thumbnail_200_{obj.image_file.name.split('/')[-1]}"
            thumbnails['thumbnail_400'] = f"{base_url}thumbnail_400_{obj.image_file.name.split('/')[-1]}"
        elif user.account_tier == CustomUser.ENTERPRISE:
            original_image_url = self.context['request'].build_absolute_uri(reverse('serve-original-image', kwargs={'image_name': obj.image_file.name.split('/')[-1]}))
            thumbnails['original_image'] = original_image_url
            thumbnails['thumbnail_200'] = f"{base_url}thumbnail_200_{obj.image_file.name.split('/')[-1]}"
            thumbnails['thumbnail_400'] = f"{base_url}thumbnail_400_{obj.image_file.name.split('/')[-1]}"
            # Logic for expiring link can be added here

        return thumbnails

class BasicImageSerializer(BaseImageSerializer):
    thumbnails = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseImageSerializer.Meta):
        fields = BaseImageSerializer.Meta.fields + ['thumbnails']

    get_thumbnails = BaseImageSerializer.get_thumbnail_urls

class PremiumImageSerializer(BasicImageSerializer):
    pass

class EnterpriseImageSerializer(BasicImageSerializer):
    pass