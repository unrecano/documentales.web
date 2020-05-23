import datetime
import os
import pymongo
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from documentaries.models import Documentary, Tag

# Database credentials.
DB_USER = os.getenv('SCRAPING_DB_USER')
DB_PASS = os.getenv('SCRAPING_DB_PASS')
DB_HOST = os.getenv('SCRAPING_DB_HOST')

# Conectar a base de datos y obtener colecciones.
uri = f"mongodb+srv://{DB_USER}:{DB_PASS}@{DB_HOST}/"
client = pymongo.MongoClient(f"{uri}?retryWrites=true&w=majority")
db = client.scraping
documentaries_collection = db.documentaries

class Command(BaseCommand):

    def _get_or_created_tags(self, tags):
        array = []
        for element in tags:
            value = slugify(element.lower())
            tag = Tag.objects.filter(value=value).first()
            if tag:
                self.stdout.write(self.style.WARNING(f"{tag.value} (existe)"))
                array.append(tag)
            else:
                new = Tag.objects.create(value=value)
                self.stdout.write(self.style.SUCCESS(f"{new.value} (creada)"))
                array.append(new)
        return array

    def handle(self, *args, **options):
        for d in documentaries_collection.find({}):
            # Verificar si el documental existe.
            # Si no existe se crea.
            slug = slugify(d.get('title'))
            documentary = Documentary.objects.filter(slug=slug).first()
            if documentary:
                self.stdout.write(self.style.WARNING(f"{documentary.title} (existe)"))
                # Si contiene un nuevo sitio se agrega al campo sites y
                # se agregan las nuevas etiquetas.
                if not d.get('site') in documentary.sites:
                    sites = documentary.sites
                    sites.append(d.get('site'))
                    documentary.sites = sites
                    # Obtener tags y agregarlas a la instancia Documentary.
                    tags = self._get_or_created_tags(d.get('tags'))
                    documentary.tags.set(tags)
                    documentary.save()
                    self.stdout.write(self.style.SUCCESS(f"{documentary.title} (actualizado)"))
            else:
                # Crear nuevos tags.
                tags = self._get_or_created_tags(d.get('tags'))
                # Crear nuevo documental.
                params = {
                    "title": d.get('title'),
                    "slug": slug,
                    "description": d.get('description'),
                    "year": d.get('year') if d.get('year') else None,
                    "duration": d.get('duration') if d.get('duration') else None,
                    "url": d.get('url'),
                    "sites": [d.get('site')],
                }
                created = Documentary.objects.create(**params)
                created.tags.set(tags)
                self.stdout.write(self.style.SUCCESS(f"{created.title} (creado)"))