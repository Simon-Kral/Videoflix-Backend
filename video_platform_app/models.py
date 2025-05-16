from django.db import models
from auth_app.models import CustomUser
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


class WatchedTime(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watched_time_user')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watched_time_video')
    watched_time = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'video',)
