# Generated by Django 5.0 on 2023-12-22 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotesapp', '0004_alter_author_born_location_alter_author_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='author',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
