from django.utils import timezone
from django.db import models
from dashboard.models import Courses


class post(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    attachment = models.FileField(upload_to='post_files', blank=True, default='')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} {self.course.Title} post'

