"""
Views for documentaries api.
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from web.models import Documentary
from .serializers import DocumentarySerializer

class DocumentaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for GET methods for Documentary.
    """
    serializer_class = DocumentarySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
        filters.OrderingFilter)
    filterset_fields = ('year', 'duration')
    search_fields = ('title', 'description')
    ordering_fields = ('year', 'title')

    def get_queryset(self):
        """
        Define queryset and add search filter.
        """
        words = self.request.GET.get('words')
        if words:
            query_words = [word.strip() for word in words.split(' ') if word]
            return Documentary.objects.search(query_words)
        return Documentary.objects.all().prefetch_related('sites')