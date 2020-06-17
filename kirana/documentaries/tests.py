from django.test import TestCase
from .models import Tag, Documentary, Url

class DocumentaryTestCase(TestCase):
    def setUp(self):
        # Crear instancias necesarias para correr los tests.
        # TODO:
        # * Los tests son para los modelos.
        # 1. Probar lista de documentales.
        # 2. Probar detalle de un documental.
        # 3. Probar paginacion.
        # 4. Busqueda de documentales.
        # 5. Filtrar documentales por etiqueta.
        # 6. Reportar enlace roto.
        documentaries = []
        for i in range(0,10):
            params = {
                    "title": f"title - {i}",
                    "slug": f"slug-{i}",
                    "description": f"description is a set of words {i}",
                    "year": f"200{i}",
                    "duration": 60 + i,
                    }
            documentary = Documentary.objects.create(**params)
            print(documentary)

    def test_list_documentaries(self):
        # pass
        self.assertTrue(True)
