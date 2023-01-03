from django.db import models

# Create your models here.
class UserUpload(models.Model):
    image = models.ImageField(upload_to='images/')

class UserCartoonify(models.Model):
    image = models.ImageField(upload_to='images/')