# Generated by Django 5.0.3 on 2024-04-06 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatroom",
            name="first_owner_deleted_time",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="second_owner_deleted_time",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
