from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='announcement', null=True)

