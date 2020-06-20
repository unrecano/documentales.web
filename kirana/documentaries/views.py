from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from .models import Documentary, Url, Point

class DocumentaryDetailView(DetailView):
    model = Documentary

    def get_template_names(self):
        return 'documentaries/detail.html'

class RedirectSiteView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(Url, id=kwargs.get('id'))
        url.add_visitor()
        return url.url

class AboutView(TemplateView):
    def get_template_names(self):
        return "documentaries/about.html"

@require_POST
def point(request):
    url = get_object_or_404(Url, id=request.POST.get('url'))
    data = {
        "url": url,
        "comment": request.POST.get('comment')
    }
    Point.objects.create(**data)
    return redirect(request.META.get('HTTP_REFERER'))