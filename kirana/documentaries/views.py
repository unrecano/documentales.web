from django.shortcuts import render, get_object_or_404, redirect
from .models import Documentary, Url

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

def about(request):
    return render(request, 'documentaries/about.html')