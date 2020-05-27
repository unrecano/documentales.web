from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Documentary, Url, Point

def detail(request, slug):
    documentary = get_object_or_404(Documentary, slug=slug)
    context = {
        "documentary": documentary
    }
    return render(request, 'documentaries/detail.html', context)

def redirect_url(request, id):
    url = get_object_or_404(Url, id=id)
    url.visitors = url.visitors + 1
    url.save()
    return redirect(url.url)

@require_POST
def point(request):
    url = get_object_or_404(Url, id=request.POST.get('url'))
    data = {
        "url": url,
        "comment": request.POST.get('comment')
    }
    Point.objects.create(**data)
    return redirect(request.META.get('HTTP_REFERER'))

def about(request):
    return render(request, 'documentaries/about.html')