from django.db import models

class LocationDetails(models.Model):
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    name = models.CharField(max_length=1500)
    # date = models.CharField(max_length=60)
    date = models.DateTimeField()

    def __str__(self):
        return self.name