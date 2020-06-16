from django.urls import resolve
from django.test import TestCase
from . import views

class HomePageTestCase(TestCase):
    def test_home_page_resolves(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, views.search.__name__)