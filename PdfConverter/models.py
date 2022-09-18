from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='converted-pdf')


class PdfFile(models.Model):
    name = models.CharField(max_length=30)


class Images(models.Model):
    PdfFile = models.ForeignKey(PdfFile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pdf-image')

