"""
Views for documentaries api.
"""
from rest_framework import viewsets
from web.models import Documentary
from .serializers import DocumentarySerializer

class DocumentaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for GET methods for Documentary.
    """
    queryset = Documentary.objects.all().prefetch_related('sites')
    serializer_class = DocumentarySerializer
