from django.urls import path, include
from rest_framework import routers
from .views import VideoViewSet

router = routers.DefaultRouter()
router.register(r'videos', VideoViewSet, basename='videos')


urlpatterns = [
    path('', include(router.urls)),
]
