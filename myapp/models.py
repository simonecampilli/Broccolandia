from django.conf import settings
from django.db import models

class UserData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reading = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username
