"""
Crawler for site: Top Documentary Films
"""
from .utils import get_html_from_url

URL_BASE = "https://topdocumentaryfilms.com"
SITE = "Top Documentary Films"

def get_document():
    """
    Obtener documento html de página principal.
    """
    return get_html_from_url(f'{URL_BASE}/all', True)

def get_documentaries_in_page(page):
    """
    Obtener listado de elementos con información de documentales de una
    página específica.

    url -- string.
    """
    url = f'{URL_BASE}/all/page/{page}/'
    document = get_html_from_url(url, True)
    return document.find_all('article', class_='module')

def get_url_documentary(documentary):
    """
    Extraer la url del detalle de un elemento documental (HTML).

    element -- string.
    """
    return documentary.find('h2').find("a").get('href')

def all_documentaries_documentarytop():
    """
    Retornar un array con todas las urls de los documentales del sitio.
    """
    document = get_document()
    _all = []
    pages = document.find("div", class_="pagination module").find_all("a")
    for i in range(1, int(pages[-2].text) + 1):
        documentaries = [get_url_documentary(d) \
            for d in get_documentaries_in_page(i)]
        _all = _all + documentaries
    return _all

def documentary_documentarytop(url):
    """
    Extraer información del detalle de un documental.

    url -- string.
    """
    html = get_html_from_url(url, True)
    main = html.find("main", {"role": "main"}).find("article")
    title = main.find("h1").text
    year = main.find("meta", {"itemprop": "dateCreated"}).get("content") \
        if main.find("meta", {"itemprop": "dateCreated"}) else None
    duration = main.find("time").text.split(" ")[0] \
        if main.find("time") else None
    tags = main.find("div", {"class": "meta-bar meta-single"}).find_all("a")
    paragraphs = main.find("div", {"itemprop": "reviewBody"}).find_all("p")
    embedded = html.find("meta", {"itemprop": "embedUrl"}).get("content") \
        if html.find("meta", {"itemprop": "embedUrl"}) else None
    return {
        "url": url,
        "site": SITE,
        "title": title,
        "year": year,
        "embedded": embedded,
        "duration": duration,
        "tags": [t.text.strip() for t in tags],
        "description": " ".join([p.text.strip() for p in paragraphs])
    }
