from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from .permissions import ReadOnly
from ..models import Category, Video, WatchedTime
from .serializers import CategorySerializer, VideoSerializer, WatchedTimeSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from .filters import VideoFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import VideoPagination
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from auth_app.models import CustomUser
from rest_framework import status

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CategoryViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly, IsAuthenticated]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VideoViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly, IsAuthenticated]

    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = VideoFilter

    ordering_fields = ['created_at']

    pagination_class = VideoPagination


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def watched_time_view(request, video_id):
    """ 
    Allows authenticated users to view or update their own profile information.
    """
    user = request.user
    video = Video.objects.get(pk=video_id)

    if request.method == 'GET':
        watchedTime = WatchedTime.objects.filter(user=user, video=video).first()
        if watchedTime:
            return Response({'watched_time': watchedTime.watched_time}, status=status.HTTP_200_OK)
        else:
            return Response({'watched_time': 0}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        watched_time = request.data['watched_time']
        try:
            instance, created = WatchedTime.objects.get_or_create(user=user, video=video, defaults={'watched_time': watched_time})
            if not created:
                instance.watched_time = watched_time
            instance.save()
            return Response({'watched_time': instance.watched_time}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Well, that didn\'t work.'}, status=status.HTTP_400_BAD_REQUEST)
