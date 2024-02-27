# Generated by Django 3.2.16 on 2024-02-26 16:32

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_comment"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="post",
            managers=[
                ("is_pub", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="posts_images", verbose_name="Фото"
            ),
        ),
    ]