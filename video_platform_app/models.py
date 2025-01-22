from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.title}'


class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='video_category')
