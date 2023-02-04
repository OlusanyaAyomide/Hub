# Generated by Django 4.1.6 on 2023-02-04 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_question_questionid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.subject')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.topic'),
        ),
    ]