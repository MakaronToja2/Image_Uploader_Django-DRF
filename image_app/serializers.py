from rest_framework import serializers
from .models import Image, CustomUser
from django.urls import reverse
import os
import shutil
from threading import Timer
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

#Serializer Used to create images
class WriteImageSerializer(serializers.ModelSerializer):
    generate_expiring_link = serializers.BooleanField(write_only=True, required=False, default=False)
    expiring_time = serializers.IntegerField(write_only=True, required=False, default=300)

    def __init__(self, *args, **kwargs):
        super(WriteImageSerializer, self).__init__(*args, **kwargs)

        # Get user from context if available
        user = self.context.get('request', {}).user if self.context else None

        # If user is not on the ENTERPRISE plan, remove certain fields
        if user and user.account_tier != CustomUser.ENTERPRISE:
            self.fields.pop('generate_expiring_link', None)
            self.fields.pop('expiring_time', None)

    class Meta:
        model = Image
        fields = ['id', 'image_file', 'upload_time', 'generate_expiring_link', 'expiring_time']

    def validate_expiring_time(self, value):
        if value < 300 or value > 30000:
            raise serializers.ValidationError("Expiring time should be between 300 and 30000 seconds")
        return value

    @staticmethod
    def delete_temp_image(expiring_path, instance):
        if os.path.exists(expiring_path):
            os.remove(expiring_path)
        instance.expiring_image_path = None
        instance.expiration_time = None
        instance.save()

    def create(self, validated_data):
        print(validated_data)
        user = self.context['request'].user
        generate_expiring_link = validated_data.pop('generate_expiring_link', False)
        expiring_time = validated_data.pop('expiring_time')

        instance = Image.objects.create(**validated_data)

        if generate_expiring_link and user.account_tier == CustomUser.ENTERPRISE:
            original_path = instance.image_file.path
            expiring_directory = os.path.join(settings.MEDIA_ROOT, 'expiring_images')

            # Ensure the directory exists
            if not os.path.exists(expiring_directory):
                os.makedirs(expiring_directory)

            # Get only the file name from the original path
            filename = os.path.basename(original_path)

            # Construct the expiring path
            expiring_path = os.path.join(expiring_directory, filename)
            shutil.copy2(original_path, expiring_path)
            # Schedule the image for deletion after 'expiring_time' seconds
            timer = Timer(expiring_time, lambda: self.delete_temp_image(expiring_path, instance))
            timer.start()

            # Set the expiration time here
            instance.expiration_time = timezone.now() + timedelta(seconds=expiring_time)
            instance.expiring_image_path = expiring_path
            instance.save()

        return instance


class BaseImageSerializer(WriteImageSerializer):
    expiration_time = serializers.DateTimeField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(BaseImageSerializer, self).__init__(*args, **kwargs)

        # Get user from context if available
        user = self.context.get('request', {}).user if self.context else None

        if user and user.account_tier != CustomUser.ENTERPRISE:
            self.fields.pop('generate_expiring_link', None)
            self.fields.pop('expiring_time', None)

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
            #Check if expiring image is still in DB
            if hasattr(obj, 'expiring_image_path') and obj.expiring_image_path:
                expiring_image_name = os.path.basename(obj.expiring_image_path)
                expiring_image_url = self.context['request'].build_absolute_uri(
                    reverse('serve-expiring-image', kwargs={'image_name': expiring_image_name}))
                thumbnails['expiring_image'] = expiring_image_url

            #Generate thumbnails
            original_image_url = self.context['request'].build_absolute_uri(reverse('serve-original-image', kwargs={'image_name': obj.image_file.name.split('/')[-1]}))
            thumbnails['original_image'] = original_image_url
            thumbnails['thumbnail_200'] = f"{base_url}thumbnail_200_{obj.image_file.name.split('/')[-1]}"
            thumbnails['thumbnail_400'] = f"{base_url}thumbnail_400_{obj.image_file.name.split('/')[-1]}"
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
