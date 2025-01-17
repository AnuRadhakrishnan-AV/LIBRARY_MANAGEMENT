# Generated by Django 4.2.14 on 2024-07-21 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("libraryapp", "0049_alter_booking_booked_on"),
    ]

    operations = [
        migrations.CreateModel(
            name="LibraryBook",
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
                ("library", models.CharField(max_length=255)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="libraryapp.book",
                    ),
                ),
                (
                    "librarian",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="libraryapp.user",
                    ),
                ),
            ],
        ),
    ]
