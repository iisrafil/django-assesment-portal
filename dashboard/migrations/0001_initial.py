# Generated by Django 3.1.4 on 2021-01-07 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('Title', models.TextField(max_length=100)),
                ('Course_code', models.CharField(max_length=10)),
                ('Enroll_key', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('Teacher', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, to='dashboard.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrolled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.courses')),
                ('Students', models.ManyToManyField(blank=True, to='users.Profile')),
            ],
        ),
    ]
