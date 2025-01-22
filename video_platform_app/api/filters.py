from django_filters import rest_framework as filters
from ..models import Video


class VideoFilter(filters.FilterSet):

    category = filters.NumberFilter(field_name='category_id')
    created_at = filters.NumberFilter(field_name='created_at')

    class Meta:
        model = Video
        fields = ['category']
