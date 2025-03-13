from django.db import models

class upload(models.Model):
    image = models.ImageField(upload_to='pics')

