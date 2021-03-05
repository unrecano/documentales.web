"""
Crawler for Site: Documententarymania.
"""
import math
from .utils import get_html_from_url

URL_BASE = 'https://www.documentarymania.com'
SITE = "Documentary Mania"

def get_document():
    """
    Obtener documento html de página principal.
    """
    return get_html_from_url(f'{URL_BASE}/home.php')

def get_documentaries_in_page(page):
    """
    Obtener listado de elementos con información de documentales de una
    página específica.

    url -- string.
    """
    paginator = '?pageNum_Recordset1='
    url = f'{URL_BASE}/home.php{paginator}{page}'
    document = get_html_from_url(url)
    return document.find_all('div', {'class': 'wthree-news-left'})

def get_url_documentary(element):
    """
    Extraer la url del detalle de un elemento documental (HTML).

    element -- string.
    """
    return element.find('h2').find('a').get('href')

def parse_duration(text):
    """
    Parse duration for documentary
    """
    if not text:
        return text
    duration = text.split(':')
    # Obtener segundos, minutos y horas.
    seconds = int(duration[-1])
    minutes = int(duration[-2]) if len(duration) > 1 else 0
    hours = int(duration[-3]) if len(duration) > 2 else 0
    # Convertir minutos a segundos.
    seconds = seconds + (minutes * 60)
    # Convertir horas a segundos.
    seconds = seconds + (hours * 60 * 60)
    # Retornar minutos.
    return math.ceil(seconds/60)

def all_documentaries_documentarymania():
    """
    Retornar un array con todas las urls de los documentales del sitio.
    """
    document = get_document()
    pages = document.find('div', {'class': 'blog-pagenat-wthree'}).find_all('a')
    last_page = pages[-1].text
    _all = []
    for i in range(0, int(last_page)):
        documentaries = [f'{URL_BASE}/{get_url_documentary(documentary)}' \
                         for documentary in get_documentaries_in_page(i)]
        _all = _all + documentaries
    return _all

def documentary_documentarymania(url):
    """
    Extraer información del detalle de un documental.

    url -- string.
    """
    html = get_html_from_url(url)
    meta = html.find('div', {"class": "s-author"}).find_all('p')[0].text
    main = html.find_all('div', {"class": "w3-agile-news-text"})[0]
    tags = html.find_all('div', {"class": "w3-agile-news-text"})[1]
    return {
        "url": url,
        "year": meta.split(' ')[0],
        "duration": parse_duration(meta.split(' ')[3]),
        "title": main.find('h3').text.strip(),
        "description": main.find('div', {'class': 'comments'}).text.strip(),
        "tags": [tag.text for tag in tags.find_all('a') if tag.text.strip()],
        "site": SITE,
    }
