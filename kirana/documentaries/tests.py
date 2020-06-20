from django.test import TestCase
from django.urls import resolve, reverse
from . import views
from .models import Tag, Documentary, Url

# TODO:
# * Los tests son para los modelos.
# 1. Probar lista de documentales.
# 2. Probar detalle de un documental.
# 3. Probar paginacion.
# 4. Busqueda de documentales.
# 5. Filtrar documentales por etiqueta.
# 6. Reportar enlace roto.

class RedirectFromHomePageTestCase(TestCase):

    fixtures = ['tags', 'documentaries', 'urls']

    def setUp(self):
        self.url = Url.objects.first()

    def test_redirect_resolves(self):
        view = resolve(reverse("redirect", args=[self.url.id]))
        self.assertEqual(view.func.__name__,
            views.RedirectSiteView.as_view().__name__)

    def test_redirect_to_documentary(self):
        visitors = self.url.visitors
        self.url.add_visitor()
        self.assertEqual(self.url.visitors, visitors + 1)