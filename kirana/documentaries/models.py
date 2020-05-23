import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    value = models.CharField(max_length=100)

class Documentary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    year = models.CharField(max_length=4)
    duration = models.PositiveIntegerField(null=True)
    url = models.URLField()
    sites = ArrayField(models.URLField())
    tags = models.ManyToManyField(Tag, related_name="documentaries")

    class Meta:
        verbose_name_plural = 'Documentaries'

    def __str__(self):
        return self.title