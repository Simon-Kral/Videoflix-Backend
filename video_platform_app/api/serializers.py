from rest_framework.serializers import ModelSerializer
from ..models import Category, Video, WatchedTime


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class WatchedTimeSerializer(ModelSerializer):
    class Meta:
        model = WatchedTime
        fields = '__all__'
