from django.core.management.base import BaseCommand, CommandError
from documentaries.models import Documentary

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('tweet'))