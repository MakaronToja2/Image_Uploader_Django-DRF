from django.db import models
from django.contrib.auth.models import User

class AccountTier(models.Model):
    name = models.CharField(max_length=50)
    thumbnail_sizes = models.JSONField()
    can_generate_expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.SET_NULL, null=True, blank=True)

class Image(models.Model):
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s Image {self.id}"

