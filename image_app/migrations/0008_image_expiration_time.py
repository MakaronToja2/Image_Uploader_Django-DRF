# Generated by Django 3.2 on 2023-10-08 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_app', '0007_image_expiring_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='expiration_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
