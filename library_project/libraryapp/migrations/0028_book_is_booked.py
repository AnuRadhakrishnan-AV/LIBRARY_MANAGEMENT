# Generated by Django 4.2.14 on 2024-07-15 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libraryapp", "0027_booking"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="is_booked",
            field=models.BooleanField(default=False),
        ),
    ]