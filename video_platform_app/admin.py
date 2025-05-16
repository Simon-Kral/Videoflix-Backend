from django.contrib import admin
from .models import Category, Video, WatchedTime

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ("title", "id")


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ("title", "id", "category__title")


class WatchedTimeAdmin(admin.ModelAdmin):
    model = WatchedTime
    list_display = ("user", "video", "watched_time")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(WatchedTime, WatchedTimeAdmin)
