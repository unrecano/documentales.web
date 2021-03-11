import logging
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from ...crawlers.documentaryaddict import \
    (all_documentaries_documentaryaddict, documentary_documentaryaddict)
from ...crawlers.documentaryheaven import \
    (all_documentaries_documentaryheaven, documentary_documentaryheaven)
from ...crawlers.documentarymania import \
    (all_documentaries_documentarymania, documentary_documentarymania)
from ...crawlers.documentarytop import \
    (all_documentaries_documentarytop, documentary_documentarytop)
from ...crawlers.documentarytube import \
    (all_documentaries_documentarytube, documentary_documentarytube)
from ...models import Documentary, Site

logger = logging.getLogger('crawler')

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--documentarytube', action='store_true',
            help='DocumentaryTube')
        parser.add_argument('--documentarymania', action='store_true',
            help='DocumentaryMania')
        parser.add_argument('--documentaryaddict', action='store_true',
            help='DocumentaryAddict')
        parser.add_argument('--documentarytop', action='store_true',
            help='Top Documentary Films')
        parser.add_argument('--documentaryheaven', action='store_true',
            help='Documentary Heaven')

    def handle(self, *args, **options):
        if options.get('documentarytube'):
            documentaries = all_documentaries_documentarytube()
            self._save_documentaries(documentaries,
                documentary_documentarytube)
        elif options.get('documentarymania'):
            documentaries = all_documentaries_documentarymania()
            self._save_documentaries(documentaries,
                documentary_documentarymania)
        elif options.get('documentaryaddict'):
            documentaries = all_documentaries_documentaryaddict()
            self._save_documentaries(documentaries,
                documentary_documentaryaddict)
        elif options.get('documentaryheaven'):
            documentaries = all_documentaries_documentaryheaven()
            self._save_documentaries(documentaries,
                documentary_documentaryheaven)
        elif options.get('documentarytop'):
            documentaries = all_documentaries_documentarytop()
            self._save_documentaries(documentaries,
                documentary_documentarytop)
    
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
                obj, created = Documentary.objects.update_or_create(
                    slug=slug,
                    defaults=d_params
                )
                if created:
                    s_params = {
                        "url": documentary.get('url'),
                        "name": documentary.get('site'),
                        "embedded": documentary.get("embedded"),
                        "documentary": obj
                    }
                    site = Site.objects.create(**s_params)
                    msg = f"{obj.title} - {site.url} (creado)"
                    self.stdout.write(self.style.SUCCESS(msg))
                else:
                    site, created = Site.objects.update_or_create(
                        name=documentary.get('site'),
                        url=documentary.get('url'),
                        defaults={
                            "documentary": obj,
                            "embedded": documentary.get("embedded")
                        }
                    )
                    msg = f"{obj.title} - {site.url} (actualizado)"
                    self.stdout.write(self.style.WARNING(msg))
            except Exception as e:
                self.stdout.write(self.style.WARNING(str(e)))
                logger.error(element + " " + str(e))
                continue
