from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView, RedirectView
from .models import Documentary, Url, Point

def detail(request, slug):
    documentary = get_object_or_404(Documentary, slug=slug)
    context = {
        "documentary": documentary
    }
    return render(request, 'documentaries/detail.html', context)

class RedirectSiteView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(Url, id=kwargs.get('id'))
        url.add_visitor()
        return url.url

@require_POST
def point(request):
    url = get_object_or_404(Url, id=request.POST.get('url'))
    data = {
        "url": url,
        "comment": request.POST.get('comment')
    }
    Point.objects.create(**data)
    return redirect(request.META.get('HTTP_REFERER'))

class AboutView(TemplateView):
    template = "documentaries/about.html"