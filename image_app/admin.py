from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Image

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'account_tier']
    list_filter = ['account_tier']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {'fields': ('account_tier',)}),
    )

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'upload_time']
