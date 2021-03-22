"""
Serializers for documentaries api.
"""
from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from web.models import Documentary, Site

class SiteSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for model Site.
    """
    class Meta:
        model = Site
        fields = ('name', 'url')

class DocumentarySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for model Documentary
    """
    sites = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Documentary
        fields = ('id', 'title', 'slug', 'description', 'year', 'duration',
            'tags', 'sites')
