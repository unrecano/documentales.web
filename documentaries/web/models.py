"""
Models for documentaries project.
"""
import uuid
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import (SearchQuery, SearchRank,
    SearchVector)
from django.db import models

class DocumentaryManager(models.Manager):
    """
    Manager for custom queries.
    """
    def search(self, words):
        """
        Full text search for documentaries and order by rank.

        Parameters:
        words - list.
        """
        vector = SearchVector('title', 'description')
        query = SearchQuery(words[0])
        for word in words[1:]:
            query = query | SearchQuery(word)
        rank = SearchRank(vector, query)
        # Retornar documentales con coincidencias.
        return self.annotate(rank=rank).filter(rank__gt=0.0).order_by('-rank')

class Documentary(models.Model):
    """
    Documentary model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    year = models.CharField(max_length=4, null=True)
    duration = models.PositiveIntegerField(null=True)
    tweeted = models.BooleanField(default=False)
    tags = ArrayField(models.CharField(max_length=255, blank=True))
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    objects = DocumentaryManager()

    class Meta:
        """
        Meta for Documentary model.
        """
        verbose_name_plural = 'Documentaries'

    @property
    def sites(self):
        """
        Return number of sites.
        """
        return self.sites.count()

    @property
    def views(self):
        """
        Return number of visitors.
        """
        return sum([site.visitors for site in self.sites.all()])

    def __str__(self):
        return str(self.title)

class Site(models.Model):
    """
    Site model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=255)
    url = models.URLField()
    embedded = models.CharField(max_length=255, null=True, blank=True)
    documentary = models.ForeignKey(Documentary, on_delete=models.CASCADE,
        related_name="sites")
    visitors = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def add_visitor(self):
        """
        Add a visitor.
        """
        self.visitors = self.visitors + 1
        self.save()

    def __str__(self):
        return str(self.url)

class Report(models.Model):
    """
    Report Model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    comment = models.TextField(null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,
        related_name="reports", null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.site)
