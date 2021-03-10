"""
Crawler for Site: Documentarytube.
"""
from .utils import get_html_from_url

URL_BASE = "http://www.documentarytube.com"
SITE = "DocumentaryTube"

def get_document():
    """
    Obtener documento html de página principal.
    """
    return get_html_from_url(f'{URL_BASE}/videos')

def get_documentaries_in_page(page):
    """
    Obtener listado de elementos con información de documentales de una
    página específica.

    url -- string.
    """
    paginator = 'page={}&per-page=24'
    url = f'{URL_BASE}/videos?{paginator.format(page + 1)}'
    document = get_html_from_url(url)
    return document.find('div', {'class': 'list-view'})\
                   .find_all('div', {'class': 'panel'})

def get_url_documentary(documentary):
    """
    Extraer la url del detalle de un elemento documental (HTML).

    element -- string.
    """
    return documentary.find('div', class_='box-title').find('a').get('href')

def all_documentaries_documentarytube():
    """
    Retornar un array con todas las urls de los documentales del sitio.
    """
    document = get_document()
    element = document.find('ul', {"class": "pagination"})
    pages = [a.find('a') for a in element if a.find('a') is not None]
    last_page = pages[-1].get('data-page')
    _all = []
    for i in range(0, int(last_page) + 1):
        documentaries = [get_url_documentary(documentary) \
                         for documentary in get_documentaries_in_page(i)]
        _all = _all + documentaries
    return _all

def documentary_documentarytube(url):
    """
    Extraer información del detalle de un documental.

    url -- string.
    """
    html = get_html_from_url(url)
    main = html.find('div', {"class": "container mt35 mb35"})
    tags = html.find('li', {"class": "category"})
    text = ""
    for _p in main.find_all('p', {'class': 'MsoNoSpacing'}):
        text = text + f' {_p.text}'
    embedded = main.find("iframe", {"id": "player"}).get("src") \
        if main.find("iframe", {"id": "player"}) else None
    return {
        "url": url,
        "title": main.find('h1').text.strip(),
        "description": text.strip(),
        "tags": [tag.text for tag in tags.find_all('a') if tag.text.strip()],
        "site": SITE,
        "embedded": embedded
    }
