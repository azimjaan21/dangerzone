from django.db import models

class PolygonZone(models.Model):
    name = models.CharField(max_length=100, default="Zone")
    points = models.JSONField()  # Stores polygon points as JSON

