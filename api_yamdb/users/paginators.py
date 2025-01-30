from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """Пагинация для пользователей."""

    page_size = 10  # Количество объектов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100
