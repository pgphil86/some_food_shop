from rest_framework.pagination import PageNumberPagination


class PagePagination(PageNumberPagination):
    """
    Настройка пагинации.
    Использует пагинацию по номерам страниц и размеру.
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
