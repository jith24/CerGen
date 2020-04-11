from django.db import models


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    sfile = models.FileField(upload_to='files/',blank=True, null=True)


    def __str__(self):
        return self.title