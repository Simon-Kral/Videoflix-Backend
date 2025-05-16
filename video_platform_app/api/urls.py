from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, VideoViewSet, watched_time_view

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'videos', VideoViewSet, basename='videos')


urlpatterns = [
    path('', include(router.urls)),
    path('watched_time/<video_id>', watched_time_view, name='watched_time'),
]
