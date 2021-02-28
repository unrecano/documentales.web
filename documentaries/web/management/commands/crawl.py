import logging
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from web.crawlers.documentarytube import \
    (all_documentaries_documentarytube, documentary_documentarytube)
from web.crawlers.documentarymania import \
    (all_documentaries_documentarymania, documentary_documentarymania)
from web.models import Documentary, Site

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
    
    def _get_tags(self, tags):
        return [slugify(tag.lower()) for tag in tags]
    
    def _save_documentaries(self, array, parser):
        for element in array:
            try:
                documentary = parser(element)
                slug = slugify(documentary.get('title'))
                d_params = {
                    "title": documentary.get('title'),
                    "slug": slug,
                    "description": documentary.get('description'),
                    "year": documentary.get('year') \
                        if documentary.get('year') else None,
                    "duration": documentary.get('duration') \
                        if documentary.get('duration') else None,
                    "tags": self._get_tags(documentary.get('tags'))
                }
                obj, created = Documentary.objects.get_or_create(
                    slug=slug,
                    defaults=d_params
                )
                if created:
                    s_params = {
                        "url": documentary.get('url'),
                        "name": documentary.get('site'),
                        "documentary": obj
                    }
                    site = Site.objects.create(**s_params)
                    msg = f"{obj.title} - {site.url} (creado)"
                    self.stdout.write(self.style.SUCCESS(msg))
                else:
                    site, created = Site.objects.get_or_create(
                        name=documentary.get('site'),
                        url=documentary.get('url'),
                        defaults={"documentary": obj}
                    )
                    msg = f"{obj.title} - {site.url} (actualizado)"
                    self.stdout.write(self.style.WARNING(msg))
            except Exception as e:
                self.stdout.write(self.style.WARNING(str(e)))
                logger.error(element + " " + str(e))
                continue