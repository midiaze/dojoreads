# Generated by Django 2.2.4 on 2021-06-22 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-updated_at']},
        ),
    ]