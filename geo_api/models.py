from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    geom = models.PointField()

    def __str__(self):
        return self.name
