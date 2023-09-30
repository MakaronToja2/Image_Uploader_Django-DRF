from django.contrib import admin
from .models import AccountTier, UserProfile, Image

admin.site.register(UserProfile)

@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'upload_time']