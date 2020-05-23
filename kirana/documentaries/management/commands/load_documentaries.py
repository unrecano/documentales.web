import datetime
import os
import pymongo
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from documentaries.models import Documentary, Tag

# # Database credentials.
# DB_USER = os.getenv('SCRAPING_DB_USER')
# DB_PASS = os.getenv('SCRAPING_DB_PASS')
# DB_HOST = os.getenv('SCRAPING_DB_HOST')

# # Conectar a base de datos y obtener colecciones.
# uri = f"mongodb+srv://{DB_USER}:{DB_PASS}@{DB_HOST}/"
# client = pymongo.MongoClient(f"{uri}?retryWrites=true&w=majority")
# db = client.scraping
# documentaries_collection = db.documentaries

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = [
            {
                '_id': '5ec89a159fbf3dbfff70c4f5',
                'url': 'https://www.documentarymania.com/player.php?title=The+Incredible+Human+Journey%3A+Asia',
                'year': '2009',
                'duration': 59,
                'title': 'The Incredible Human Journey: Asia',
                'description': "The journey continues into Asia, the world's greatest land mass, in a quest to discover how early hunter-gatherers managed to survive in one of the most inhospitable places on earth - the Arctic region of Northern Siberia. Alice also explores what may have occurred during human migration to produce Chinese physical characteristics, and considers a controversial claim about Chinese evolution: that the Chinese do not share the same African ancestry as other peoples.",
                'tags': ['History', 'Prehistory', 'Evolution', 'Genetics', 'Homo sapiens', 'Siberia China', 'Asia', 'The Incredible Human Journey'],
                'site': 'https://www.documentarymania.com',
                'inserted_at': datetime.datetime(2020, 5, 22, 22, 35, 49, 401000)
            },
            {
                '_id': '5ec89a169fbf3dbfff70c4f6',
                'url': 'https://www.documentarymania.com/player.php?title=The+Incredible+Human+Journey%3A+Australia',
                'year': '2009',
                'duration': 59,
                'title': 'The Incredible Human Journey: Australia',
                'description': "Dr Alice Roberts looks at our ancestors' seemingly impossible journey to Australia. Miraculously preserved footprints and very old human fossils buried in the outback suggest a mystery: that humans reached Australia almost before anywhere else. How could they have travelled so far from Africa, crossing the open sea on the way, and do it thousands of years before they made it to Europe? The evidence trail is faint and difficult to pick up, but Alice takes on the challenge. In India, new discoveries among the debris of a super volcano hint that our species started the journey much earlier than previously thought, while in Malaysia, genetics points to an ancient trail still detectable in the DNA of tribes today.\r\nAlice travels deep into the Asian rainforests in search of the first cavemen of Borneo and tests out a Stone Age raft to see whether sea travel would have been possible thousands of years ago, before coming to a powerful conclusion.",
                'tags': ['History', 'Prehistory', 'Evolution', 'Genetics', 'Homo sapiens', 'Australia', 'The Incredible Human Journey'],
                'site': 'https://www.documentarymania.com',
                'inserted_at': datetime.datetime(2020, 5, 22, 22, 35, 50, 888000)
            }
        ]
        self.stdout.write(self.style.SUCCESS("Cargando ..."))
        for documentary in data:
            print(documentary)