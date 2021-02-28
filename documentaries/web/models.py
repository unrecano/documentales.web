import uuid
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import (SearchQuery, SearchRank,
    SearchVector)
from django.db import models

class DocumentaryManager(models.Manager):
    def search(self, words):
        vector = SearchVector('title', 'description')
        query = SearchQuery(words[0])
        for word in words[1:]:
            query = query | SearchQuery(word)
        rank = SearchRank(vector, query)
        # Retornar documentales con coincidencias.
        return self.annotate(rank=rank).filter(rank__gt=0.0).order_by('-rank')

class Documentary(models.Model):
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
        verbose_name_plural = 'Documentaries'

    @property
    def sites(self):
        return self.sites.count()

    @property
    def views(self):
        return sum([site.visitors for site in self.sites.all()])

    def __str__(self):
        return str(self.title)

class Site(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=255)
    url = models.URLField()
    documentary = models.ForeignKey(Documentary, on_delete=models.CASCADE,
        related_name="sites")
    visitors = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def add_visitor(self):
        self.visitors = self.visitors + 1
        self.save()

    def __str__(self):
        return str(self.url)

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    comment = models.TextField(null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,
        related_name="reports", null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.site)
