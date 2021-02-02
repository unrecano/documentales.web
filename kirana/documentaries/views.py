from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from .models import Documentary, Site, Report

class DocumentaryDetailView(DetailView):
    model = Documentary

    def get_template_names(self):
        return 'documentaries/detail.html'

class ToSiteRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(Site, id=kwargs.get('id'))
        url.add_visitor()
        return url.url

class AboutView(TemplateView):
    def get_template_names(self):
        return "documentaries/about.html"

class ReportDocumentaryView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST.get('site'))
        site = get_object_or_404(Site, id=request.POST.get('site'))
        data = {
            "site": site,
            "comment": request.POST.get('comment')
        }
        Report.objects.create(**data)
        return redirect(request.META.get('HTTP_REFERER'))