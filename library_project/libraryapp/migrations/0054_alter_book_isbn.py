# Generated by Django 4.2.14 on 2024-07-21 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libraryapp", "0053_alter_book_isbn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(max_length=13),
        ),
    ]