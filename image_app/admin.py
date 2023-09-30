from django.contrib import admin
from .models import AccountTier, UserProfile, Image

admin.site.register(AccountTier)
admin.site.register(UserProfile)
admin.site.register(Image)