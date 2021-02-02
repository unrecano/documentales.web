from django.test import TestCase
from django.urls import resolve, reverse
from . import views
from .models import Documentary, Site

class RedirectFromHomePageTestCase(TestCase):
    fixtures = ['documentaries', 'sites']

    def setUp(self):
        self.site = Site.objects.first()

    def test_redirect_resolves(self):
        view = resolve(reverse("redirect", args=[self.site.id]))
        self.assertEqual(view.func.__name__,
            views.ToSiteRedirectView.as_view().__name__)

    def test_redirect_to_documentary(self):
        visitors = self.site.visitors
        self.site.add_visitor()
        self.assertEqual(self.site.visitors, visitors + 1)

class DocumentaryDetailTestCase(TestCase):
    fixtures = ['documentaries', 'sites']

    def test_detail_resolves(self):
        documentary = Documentary.objects.first()
        view = resolve(reverse("detail", args=[documentary.slug]))
        self.assertEqual(view.func.__name__,
            views.DocumentaryDetailView.as_view().__name__)

class AboutPageTestCase(TestCase):
    def test_about_resolves(self):
        view = resolve("/about/")
        self.assertEqual(view.func.__name__,
            views.AboutView.as_view().__name__)

class ReportDocumentaryTestCase(TestCase):
    def test_report_documentary_resolves(self):
        view = resolve("/report/")
        self.assertEqual(view.func.__name__,
            views.ReportDocumentaryView.as_view().__name__)