# Generated by Django 4.2.14 on 2024-07-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libraryapp", "0016_rename_librarian_name_library_librarian"),
    ]

    operations = [
        migrations.AlterField(
            model_name="library",
            name="librarian",
            field=models.CharField(max_length=100),
        ),
    ]