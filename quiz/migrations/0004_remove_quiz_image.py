# Generated by Django 3.1.4 on 2021-01-15 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20210116_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='image',
        ),
    ]