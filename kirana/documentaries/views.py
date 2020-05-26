from django.shortcuts import render, get_object_or_404
from .models import Documentary

def detail(request, slug):
    documentary = get_object_or_404(Documentary, slug=slug)
    context = {
        "documentary": documentary
    }
    return render(request, 'documentaries/detail.html', context)

def about(request):
    return render(request, 'documentaries/about.html')