
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр в запросе для указания размера страницы
    max_page_size = 100  # Максимальное количество элементов на странице
