from django.conf import settings
from django.db import models

# models.py
from django.db import models

class UserData(models.Model):
    comune = models.CharField(max_length=255)
    indirizzo = models.CharField(max_length=255)
    civ = models.CharField(max_length=50, blank=True, null=True)
    codice_letturista = models.CharField(max_length=50)
    data_lettura = models.DateField()
    ora_lettura = models.TimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(blank=True, null=True)
    lettura1 = models.IntegerField(blank=True, null=True)
    lettura2 = models.IntegerField(blank=True, null=True)
    lettura3 = models.IntegerField(blank=True, null=True)
    link_map = models.URLField(max_length=500, blank=True, null=True)
    flag = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.comune} - {self.indirizzo}"


