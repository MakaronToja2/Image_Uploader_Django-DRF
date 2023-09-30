from django.db import models
from django.contrib.auth.models import AbstractUser

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
    image_file = models.ImageField(upload_to='images/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Image {self.id}"
