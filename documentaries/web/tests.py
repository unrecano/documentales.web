"""
Tests for Documentaries project.
"""
from django.test import TestCase
from django.urls import resolve, reverse
from . import views
from .models import Documentary, Site

class RedirectFromHomePageTestCase(TestCase):
    """
    Test case redirect from Home page.
    """
    fixtures = ['documentaries', 'sites']

    def setUp(self):
        """
        Init Test case.
        """
        self.site = Site.objects.first()

    def test_redirect_resolves(self):
        """
        Assert if view is correct.
        """
        view = resolve(reverse("redirect", args=[self.site.id]))
        self.assertEqual(view.func.__name__,
            views.ToSiteRedirectView.as_view().__name__)

    def test_redirect_to_documentary(self):
        """
        Assert if visitor add one.
        """
        visitors = self.site.visitors
        self.site.add_visitor()
        self.assertEqual(self.site.visitors, visitors + 1)

class DocumentaryDetailTestCase(TestCase):
    """
    Test case for Documentary detail.
    """
    fixtures = ['documentaries', 'sites']

    def test_detail_resolves(self):
        """
        Assert if view is correct.
        """
        documentary = Documentary.objects.first()
        view = resolve(reverse("detail", args=[documentary.slug]))
        self.assertEqual(view.func.__name__,
            views.DocumentaryDetailView.as_view().__name__)

class AboutPageTestCase(TestCase):
    """
    Test case for About page.
    """
    def test_about_resolves(self):
        """
        Assert if view is correct.
        """
        view = resolve("/about/")
        self.assertEqual(view.func.__name__,
            views.AboutView.as_view().__name__)

class ReportDocumentaryTestCase(TestCase):
    """
    Test case for Report.
    """
    def test_report_documentary_resolves(self):
        """
        Assert if view is correct.
        """
        view = resolve("/report/")
        self.assertEqual(view.func.__name__,
            views.ReportDocumentaryView.as_view().__name__)

class HomePageTestCase(TestCase):
    """
    Test case for Home page.
    """
    fixtures = ['documentaries', 'sites']

    def test_home_page_resolves(self):
        """
        Assert if view is correct.
        """
        view = resolve('/')
        self.assertEqual(view.func.__name__,
            views.SearchDocumentaryView.as_view().__name__)

    def test_search_documentaries(self):
        """
        Assert if search is correct.
        """
        words = ['world', 'ranger']
        documentaries = Documentary.objects.search(words)
        self.assertEqual(documentaries.count(), 2)
