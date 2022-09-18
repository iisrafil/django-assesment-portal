from django.db import models
from users.models import Profile
from django.urls import reverse


class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user.username} t_Profile'


class Courses(models.Model):
    Title = models.CharField(max_length=200)
    Course_code = models.CharField(max_length=10)
    Enroll_key = models.CharField(max_length=15, primary_key=True)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default='admin')

    def __str__(self):
        return f'{self.Title}'

    def get_absolute_url(self):
        return reverse('dashboard-home')


class CourseEnrolled(models.Model):
    Course = models.OneToOneField(Courses,on_delete=models.CASCADE)
    Students = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return f'{self.Course.Title}'

