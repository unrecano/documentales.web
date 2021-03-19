"""
Serializers for documentaries api.
"""
from rest_framework import serializers
from web.models import Documentary, Site

class SiteSerializer(serializers.ModelSerializer):
    """
    Serializer for model Site.
    """
    class Meta:
        model = Site
        fields = ('name', 'url')

class DocumentarySerializer(serializers.ModelSerializer):
    """
    Serializer for model Documentary
    """
    sites = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Documentary
        fields = ('id', 'title', 'slug', 'description', 'year', 'duration',
            'tags', 'sites')
