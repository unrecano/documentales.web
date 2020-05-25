from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.paginator import Paginator
from django.shortcuts import render
from documentaries.models import Documentary

def search(request):
    # Obtener palabras por buscar.
    words = request.GET.get('query')
    documentaries = []
    if words:
        # Crear vector con palabras para buscar.
        query_words = [word.strip() for word in words.split(' ') if word]
        vector = SearchVector('title', 'description')
        query = SearchQuery(query_words[0])
        for word in query_words[1:]:
            query = query | SearchQuery(word)
        rank = SearchRank(vector, query)
        # Retornar documentales con coincidencias.
        documentaries = Documentary.objects.annotate(rank=rank)\
                                           .filter(rank__gt=0.0)\
                                           .order_by('-rank')
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