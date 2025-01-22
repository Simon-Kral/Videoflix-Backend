from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .tasks import convert, delete
import django_rq
import os


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert, instance=instance)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(delete, instance=instance)
        # delete(instance)
        print('Video deleted')
