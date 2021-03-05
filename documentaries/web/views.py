"""
Views for Documentaries project.
"""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from .models import Documentary, Site, Report

class DocumentaryDetailView(DetailView):
    """
    Show a documentary.
    """
    model = Documentary

    def get_template_names(self):
        """
        Return template for a documentary.
        """
        return 'documentaries/detail.html'

class ToSiteRedirectView(RedirectView):
    """
    Redirect to site.
    """
    def get_redirect_url(self, *args, **kwargs):
        """
        Return url for redirect.
        """
        url = get_object_or_404(Site, id=kwargs.get('id'))
        url.add_visitor()
        return url.url

class AboutView(TemplateView):
    """
    Show about page.
    """
    def get_template_names(self):
        """
        Return template for about page.
        """
        return "documentaries/about.html"

class ReportDocumentaryView(View):
    """
    Report a issue for site.
    """
    def post(self, request):
        """
        Post request for save a report.

        request - Django request.
        """
        site = get_object_or_404(Site, id=request.POST.get('site'))
        data = {
            "site": site,
            "comment": request.POST.get('comment')
        }
        Report.objects.create(**data)
        return redirect(request.META.get('HTTP_REFERER'))

class SearchDocumentaryView(View):
    """
    Search documentaries.
    """
    def get(self, request):
        """
        Return search template with results.

        request - Django request.
        """
        # Obtener palabras por buscar.
        words = request.GET.get('query')
        documentaries = []
        if words:
            documentaries = self.__get_documentaries_in_search(words)
        else:
            # Retornar todos los documentales.
            documentaries = Documentary.objects.all()
        # Paginar el restultado.
        elements = self.__get_documentaries_per_page(request, documentaries)
        # Retornar documentales y palabras por buscar.
        context = {
            "documentaries": elements,
            "words": words if words else ''
        }
        return render(request, 'documentaries/search.html', context)

    @classmethod
    def __get_documentaries_per_page(cls, request, documentaries):
        """
        Return paginator for documentaries.

        request - Django request.
        documentaries - Documentary Queryset.
        """
        paginator = Paginator(documentaries, 24)
        page = request.GET.get('page')
        return paginator.get_page(page)

    @classmethod
    def __get_documentaries_in_search(cls, words):
        """
        Split words and return Documentaries.

        words - str.
        """
        # Crear vector con palabras para buscar.
        query_words = [word.strip() for word in words.split(' ') if word]
        # Retornar documentaries.
        return Documentary.objects.search(query_words)
