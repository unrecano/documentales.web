"""
Crawler for site: Documentary Addict
"""
from web.crawlers.utils import get_html_from_url

URL_BASE = "https://documentaryaddict.com"
SITE = "Documentary Addict"

def get_document():
    """
    Obtener documento html de página principal.
    """
    return get_html_from_url(f'{URL_BASE}/films')

def get_documentaries_in_page(page):
    """
    Obtener listado de elementos con información de documentales de una
    página específica.

    url -- string.
    """
    url = f'{URL_BASE}/films?page={page}'
    document = get_html_from_url(url)
    return document.find_all("div", {"class": "widget-film"})

def get_url_documentary(documentary):
    """
    Extraer la url del detalle de un elemento documental (HTML).

    element -- string.
    """
    return documentary.find('div', class_='caption').find('a').get('href')

def all_documentaries_documentaryaddict():
    document = get_document()
    all = []
    page = document.find("ul", {"class": "pagination"}).find_all("a")[-1]
    for i in range(1, int(page.get("href").split("=")[-1]) + 1):
        documentaries = [get_url_documentary(d) \
            for d in get_documentaries_in_page(i)]
        all = all + documentaries
    return all
        

def documentary_documentaryaddict(url):
    """
    Extraer información del detalle de un documental.

    url -- string.
    """
    html = get_html_from_url(url)
    main = html.find("div", {"id": "content-wrapper"})
    title = main.find("h1").text
    tags = main.find("span", {"class": "keywords"}).text.split(",")
    description = main.find("main", {"role": "main"}).text
    return {
        "url": url,
        "site": SITE,
        "title": title,
        "tags": [t.strip() for t in tags],
        "description": description.strip()
    }