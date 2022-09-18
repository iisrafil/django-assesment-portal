from django.db import models
from dashboard.models import Courses
from users.models import Profile
from django.utils import timezone


class Assignment(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Question = models.TextField(max_length=400)
    image = models.ImageField(upload_to='Assignment_pics', blank=True)
    file = models.FileField(upload_to='Assignment_files', blank=True)
    last_date_of_submission = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.Title}'


class AssignmentAns(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submited_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.TextField(max_length=1000, blank=True)
    ans_file = models.FileField(upload_to='Submited_files', blank=True)

    def __str__(self):
        return f'{self.submited_by} {self.assignment.Title} answer'

