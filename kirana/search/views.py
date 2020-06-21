from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import View
from documentaries.models import Documentary, Tag
from search.models import Search

class SearchDocumentaryView(View):
    def get(self, request, *args, **kwargs):
        # Obtener palabras por buscar.
        words = request.GET.get('query')
        tag = request.GET.get('tag')
        documentaries = []
        if words:
            documentaries = self.__get_documentaries_in_search(words)
        elif tag:
            documentaries = self.__get_documentaries_with_tag(tag)
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
        return render(request, 'search/search.html', context)

    def __get_documentaries_per_page(self, request, documentaries):
        paginator = Paginator(documentaries, 24)
        page = request.GET.get('page')
        return paginator.get_page(page)

    def __get_documentaries_in_search(self, words):
        # Crear vector con palabras para buscar.
        query_words = [word.strip() for word in words.split(' ') if word]
        # Guardar palabras.
        search = Search.objects.create(words=query_words)
        # Retornar documentaries.
        documentaries = Documentary.objects.search(query_words)
        # Guardar resultados.
        search.documentaries.set(documentaries)
        return documentaries

    def __get_documentaries_with_tag(self, tag):
        # Buscar documentales que contengan la etiqueta.
        obj = get_object_or_404(Tag, value=tag)
        return Documentary.objects.filter(tags=obj)