from django.contrib import admin
from .models import Category, Video

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ("title", "id")


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ("title", "id", "category__title")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)
