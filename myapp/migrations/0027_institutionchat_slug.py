# Generated by Django 4.1.6 on 2023-02-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_alter_instituition_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionchat',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
    ]
