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
        self.assertEqual(view.func.__name__, views.redirect_url.__name__)

    def test_redirect_to_documentary(self):
        visitors = self.url.visitors
        self.url.add_visitor()
        self.assertEqual(self.url.visitors, visitors + 1)

class DetailDocumentaryTestCase(TestCase):

    fixtures = ['tags', 'documentaries', 'urls']

    def test_detail_resolves(self):
        documentary = Documentary.objects.first()
        view = resolve(reverse("detail", args=[documentary.slug]))
        self.assertEqual(view.func.__name__, views.detail.__name__)

class AboutPageTestCase(TestCase):
    def test_about_resolves(self):
        view = resolve("/about")
        self.assertEqual(view.func.__name__, views.about.__name__)

class PointDocumentaryTestCase(TestCase):
    def test_point_resolves(self):
        view = resolve("/point")
        self.assertEqual(view.func.__name__, views.point.__name__)