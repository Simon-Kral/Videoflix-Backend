from rest_framework import pagination


class VideoPagination(pagination.PageNumberPagination):
    """
    Custom pagination class for paginating offers.

    Attributes:
        - page_size: Default number of offers per page.
        - page_size_query_param: Query parameter name for customizing the page size.
        - max_page_size: Maximum number of offers allowed per page.
    """
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
