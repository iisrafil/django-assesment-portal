# Generated by Django 3.1.4 on 2021-01-14 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterField(
            model_name='quiz',
            name='image',
            field=models.ImageField(upload_to='quiz_pics'),
        ),
    ]