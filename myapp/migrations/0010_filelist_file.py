# Generated by Django 4.1.6 on 2023-02-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_institutionchat_groupadmins_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filelist',
            name='file',
            field=models.FileField(default='null', upload_to='store/pdf'),
            preserve_default=False,
        ),
    ]
