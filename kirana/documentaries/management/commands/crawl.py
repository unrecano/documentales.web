import logging
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from documentaries.crawlers.documentarytube import \
    (all_documentaries_documentarytube, documentary_documentarytube)
from documentaries.crawlers.documentarymania import \
    (all_documentaries_documentarymania, documentary_documentarymania)
from documentaries.models import Documentary, Tag, Site

logger = logging.getLogger('crawler')

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--documentarytube', action='store_true',
            help='DocumentaryTube')
        parser.add_argument('--documentarymania', action='store_true',
            help='DocumentaryMania')

    def handle(self, *args, **options):
        if options.get('documentarytube'):
            documentaries = all_documentaries_documentarytube()
            self._save_documentaries(documentaries,
                documentary_documentarytube)
        elif options.get('documentarymania'):
            documentaries = all_documentaries_documentarymania()
            self._save_documentaries(documentaries,
                documentary_documentarymania)
    
    def _get_or_created_tags(self, tags):
        array = []
        for element in tags:
            value = slugify(element.lower())
            tag, created = Tag.objects.get_or_create(value=value)
            array.append(tag)
            if created:
                self.stdout.write(self.style.WARNING(f"{tag.value} (existe)"))
            else:
                self.stdout.write(self.style.SUCCESS(f"{tag.value} (creada)"))
        return array
    
    def _save_documentaries(self, array, parser):
        for element in array:
            try:
                documentary = parser(element)
                # Verificar si el documental existe.
                # Si no existe se crea.
                slug = slugify(documentary.get('title'))
                # Crear nuevo documental.
                documentary_params = {
                    "title": documentary.get('title'),
                    "slug": slug,
                    "description": documentary.get('description'),
                    "year": documentary.get('year') if documentary.get('year') else None,
                    "duration": documentary.get('duration') if documentary.get('duration') else None
                }
                obj, created = Documentary.objects.get_or_create(
                    slug=slug,
                    defaults=documentary_params
                )
                if created:
                    # Crear nuevos tags.
                    tags = self._get_or_created_tags(documentary.get('tags'))
                    obj.tags.set(tags)
                    # Crear nueva url.
                    url_params = {
                        "url": documentary.get('url'),
                        "name": documentary.get('site'),
                        "documentary": obj
                    }
                    site = Site.objects.create(**url_params)
                    # Imprime log.
                    msg = f"{obj.title} - {site.url} (creado)"
                    self.stdout.write(self.style.SUCCESS(msg))
                else:
                    # Si contiene un nuevo sitio se agrega al campo sites y
                    # se agregan las nuevas etiquetas.
                    site, created = Site.objects.get_or_create(
                        name=documentary.get('site'),
                        url=documentary.get('url'),
                        defaults={"documentary": obj}
                    )
                    tags = self._get_or_created_tags(documentary.get('tags'))
                    obj.tags.set(tags)
                    # Imprime log.
                    msg = f"{obj.title} - {site.url} (actualizado)"
                    self.stdout.write(self.style.WARNING(msg))
                print(obj)
            except Exception as e:
                self.stdout.write(self.style.WARNING(str(e)))
                logger.error(element + " " + str(e))
                continue