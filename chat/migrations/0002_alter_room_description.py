# Generated by Django 3.2 on 2021-05-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.CharField(default='Chat with your course instructor and course mate', max_length=100),
        ),
    ]