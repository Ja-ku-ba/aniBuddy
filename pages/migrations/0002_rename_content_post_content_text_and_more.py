# Generated by Django 5.0.2 on 2024-02-27 20:27

import pages.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='content_text',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='description',
            new_name='description_char',
        ),
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=pages.models.get_image_filepath),
        ),
    ]
