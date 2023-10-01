from rest_framework import serializers
from .models import Image, CustomUser
import os

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
        base_dir = os.path.dirname(obj.image_file.path)

        def thumbnail_exists(name):
            thumb_path = os.path.join(
                base_dir,
                f"{name}_{os.path.basename(obj.image_file.name)}"
            )
            return os.path.exists(thumb_path)

        if user.account_tier == CustomUser.BASIC:
            if thumbnail_exists('thumbnail_200'):
                thumbnails['thumbnail_200'] = obj.image_file.url.replace("images/", "images/thumbnail_200_")
        elif user.account_tier == CustomUser.PREMIUM:
            if thumbnail_exists('thumbnail_200'):
                thumbnails['thumbnail_200'] = obj.image_file.url.replace("images/", "images/thumbnail_200_")
            if thumbnail_exists('thumbnail_400'):
                thumbnails['thumbnail_400'] = obj.image_file.url.replace("images/", "images/thumbnail_400_")
        elif user.account_tier == CustomUser.ENTERPRISE:
            if thumbnail_exists('thumbnail_200'):
                thumbnails['thumbnail_200'] = obj.image_file.url.replace("images/", "images/thumbnail_200_")
            if thumbnail_exists('thumbnail_400'):
                thumbnails['thumbnail_400'] = obj.image_file.url.replace("images/", "images/thumbnail_400_")
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