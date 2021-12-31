from django.db import models
from django.conf import settings

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=254)
    alt = models.CharField(max_length=254, default=name)
    image = models.ImageField()

    def __str__(self):
        return self.name

class Video(models.Model):
    caption = models.CharField(max_length=254)
    video = models.FileField()

    def __str__(self):
        return self.caption