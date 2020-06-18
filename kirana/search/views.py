from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from documentaries.models import Documentary, Tag
from search.models import Search

def search(request):
    # Obtener palabras por buscar.
    words = request.GET.get('query')
    query_tag = request.GET.get('tag')
    documentaries = []
    if words:
        # Crear vector con palabras para buscar.
        query_words = [word.strip() for word in words.split(' ') if word]
        # Guardar palabras.
        search = Search.objects.create(words=query_words)
        # Retornar documentaries.
        Documentary.objects.search(query_words)
        # Guardar resultados.
        search.documentaries.set(documentaries)
    elif query_tag:
        # Buscar documentales que contengan la etiqueta.
        tag = get_object_or_404(Tag, value=query_tag)
        documentaries = Documentary.objects.filter(tags=tag)
    else:
        # Retornar todos los documentales.
        documentaries = Documentary.objects.all()
    # Paginar el restultado.
    paginator = Paginator(documentaries, 24)
    page = request.GET.get('page')
    elements = paginator.get_page(page)
    # Retornar documentales y palabras por buscar.
    context = {
        "documentaries": elements,
        "words": words if words else ''
    }
    return render(request, 'search/search.html', context)