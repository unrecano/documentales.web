from django.contrib.postgres import search
from django.core.management.base import BaseCommand, CommandError
from django.contrib.postgres.search import SearchVector
from ...models import Documentary

class Command(BaseCommand):
    def handle(self, *args, **options):
        Documentary.objects.update(search_vector=SearchVector('title', 'description'))