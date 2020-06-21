from django.urls import resolve
from django.test import TestCase
from documentaries.models import Documentary
from . import views

class HomePageTestCase(TestCase):
    fixtures = ['tags', 'documentaries', 'urls']

    def test_home_page_resolves(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__,
            views.SearchDocumentaryView.as_view().__name__)

    def test_search_documentaries(self):
        words = ['world', 'ranger']
        documentaries = Documentary.objects.search(words)
        self.assertEqual(documentaries.count(), 2)