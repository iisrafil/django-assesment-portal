# Generated by Django 3.1.4 on 2021-01-07 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.TextField(max_length=100)),
                ('Question', models.CharField(max_length=400)),
                ('image', models.ImageField(blank=True, upload_to='Assignment_pics')),
                ('file', models.FileField(blank=True, upload_to='Assignment_files')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.courses')),
            ],
        ),
    ]
