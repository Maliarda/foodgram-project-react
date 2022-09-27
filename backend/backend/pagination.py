from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPaginator(PageNumberPagination):
    """Пагинация с перееопределением названия поля."""

    page_size_query_param = "limit"
