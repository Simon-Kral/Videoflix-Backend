from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from .permissions import ReadOnly
from ..models import Category, Video
from .serializers import CategorySerializer, VideoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .filters import VideoFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CategoryViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly, IsAuthenticated]
#
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class VideoViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly, IsAuthenticated]
#
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = VideoFilter

    ordering_fields = ['created_at']

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
