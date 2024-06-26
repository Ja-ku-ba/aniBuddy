# Generated by Django 5.0.3 on 2024-03-31 12:33

import pages.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_owner_deleted_time",
                    models.DateTimeField(auto_now=True, null=True),
                ),
                (
                    "second_owner_deleted_time",
                    models.DateTimeField(auto_now=True, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Coment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("coment", models.CharField(max_length=1023)),
                ("added", models.DateTimeField()),
                ("deleted", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["-added"],
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        null=True,
                        verbose_name="Tytuł char",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        blank=True, null=True, verbose_name="Zawartość text"
                    ),
                ),
                ("added", models.DateTimeField()),
                ("deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="PostImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to=pages.models.get_image_filepath,
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Reaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reaction", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="UserMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("sent", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
