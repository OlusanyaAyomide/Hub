# Generated by Django 4.1.6 on 2023-02-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_publicquestion_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userverify',
            name='resetPassword',
            field=models.IntegerField(),
        ),
    ]
