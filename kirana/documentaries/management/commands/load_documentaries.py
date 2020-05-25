import datetime
import os
import pymongo
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from documentaries.models import Documentary, Tag, Url

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
                # Si contiene un nuevo sitio se agrega al campo sites y
                # se agregan las nuevas etiquetas.
                params = {
                    "site": d.get('site'),
                    "url": d.get('url'),
                    "documentary": documentary
                }
                url = Url.objects.filter(**params).first()
                if not url:
                    # Crear nueva url.
                    url = Url.objects.create(**params)
                    # Obtener tags y agregarlas a la instancia Documentary.
                    tags = self._get_or_created_tags(d.get('tags'))
                    documentary.tags.set(tags)
                    documentary.save()
                    # Imprime log.
                    msg = f"{documentary.title} - {url.url} (actualizado)"
                    self.stdout.write(self.style.WARNING(msg))
            else:
                # Crear nuevos tags.
                tags = self._get_or_created_tags(d.get('tags'))
                # Crear nuevo documental.
                documentary_params = {
                    "title": d.get('title'),
                    "slug": slug,
                    "description": d.get('description'),
                    "year": d.get('year') if d.get('year') else None,
                    "duration": d.get('duration') if d.get('duration') else None
                }
                created = Documentary.objects.create(**documentary_params)
                created.tags.set(tags)
                # Crear nueva url.
                url_params = {
                    "url": d.get('url'),
                    "site": d.get('site'),
                    "documentary": created
                }
                url = Url.objects.create(**url_params)
                # Imprime log.
                msg = f"{created.title} - {url.url} (creado)"
                self.stdout.write(self.style.SUCCESS(msg))