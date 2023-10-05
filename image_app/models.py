from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from PIL import Image as PilImage
import os

class CustomUser(AbstractUser):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    ENTERPRISE = 'Enterprise'

    ACCOUNT_TIERS = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    ]

    account_tier = models.CharField(
        max_length=20,
        choices=ACCOUNT_TIERS,
        default=BASIC,
    )

    def __str__(self):
        return self.username

class Image(models.Model):
    user = models.ForeignKey(CustomUser, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Image {self.id}"

    def save(self, *args, **kwargs):
        # Validate file extension
        valid_extensions = ['png', 'jpg']
        file_extension = self.image_file.name.split('.')[-1]
        if file_extension.lower() not in valid_extensions:
            raise ValidationError("Unsupported file extension. Use PNG or JPG.")

        super().save(*args, **kwargs)  # Call the original save method
        img = PilImage.open(self.image_file.path)

        thumbnail_sizes = {}

        if self.user.account_tier == CustomUser.BASIC:
            thumbnail_sizes['thumbnail_200'] = (200, 200)
        elif self.user.account_tier == CustomUser.PREMIUM:
            thumbnail_sizes['thumbnail_200'] = (200, 200)
            thumbnail_sizes['thumbnail_400'] = (400, 400)
        elif self.user.account_tier == CustomUser.ENTERPRISE:
            thumbnail_sizes['thumbnail_200'] = (200, 200)
            thumbnail_sizes['thumbnail_400'] = (400, 400)
            # Add more sizes or special features here if needed

        for name, size in thumbnail_sizes.items():
            thumb = img.resize(size, PilImage.LANCZOS)
            thumb_path = os.path.join(
                os.path.dirname(self.image_file.path),
                f"{name}_{os.path.basename(self.image_file.name)}"
            )
            thumb.save(thumb_path)