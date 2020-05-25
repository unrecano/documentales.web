from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Documentary

def home(request):
    documentaries = Documentary.objects.all()
    paginator = Paginator(documentaries, 24)
    page = request.GET.get('page')
    elements = paginator.get_page(page)
    context = {
        "documentaries": elements
    }
    return render(request, 'documentaries/home.html', context)