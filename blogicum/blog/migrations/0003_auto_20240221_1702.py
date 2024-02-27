# Generated by Django 3.2.16 on 2024-02-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_auto_20240203_1203"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.AlterModelOptions(
            name="location",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "местоположение",
                "verbose_name_plural": "Местоположения",
            },
        ),
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-pub_date"],
                "verbose_name": "публикация",
                "verbose_name_plural": "Публикации",
            },
        ),
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="birthdays_images", verbose_name="Фото"
            ),
        ),
    ]