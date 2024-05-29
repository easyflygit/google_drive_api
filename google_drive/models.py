from django.db import models


class File(models.Model):
    name = models.CharField(max_length=255)
    data = models.TextField()

    class Meta:
        app_label = 'google_drive'