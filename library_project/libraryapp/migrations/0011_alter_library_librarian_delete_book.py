# Generated by Django 4.2.14 on 2024-07-14 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libraryapp", "0010_library_librarian"),
    ]

    operations = [
        migrations.AlterField(
            model_name="library",
            name="librarian",
            field=models.CharField(default="Default Librarian", max_length=100),
        ),
        migrations.DeleteModel(
            name="Book",
        ),
    ]