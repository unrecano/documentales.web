from documentaries.crawlers.utils import get_html_from_url

url_base = "http://www.documentarytube.com"
site = "DocumentaryTube"

def get_document():
    """
    Obtener documento html de página principal.
    """
    return get_html_from_url(f'{url_base}/videos')

def get_documentaries_in_page(url):
    """
    Obtener listado de elementos con información de documentales de una
    página específica.

    url -- string.
    """
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
    paginator = 'page={}&per-page=24'
    document = get_document()
    element = document.find('ul', {"class": "pagination"})
    pages = [a.find('a') for a in element if a.find('a') != None]
    last_page = pages[-1].get('data-page')
    all = []
    for i in range(0, int(last_page) + 1):
        url = f'{url_base}/videos?{paginator.format(i + 1)}'
        documentaries = [get_url_documentary(documentary) \
                         for documentary in get_documentaries_in_page(url)]
        all = all + documentaries
    return all

def documentary_documentarytube(url):
    """
    Extraer información del detalle de un documental.

    url -- string.
    """
    html = get_html_from_url(url)
    main = html.find('div', {"class": "container mt35 mb35"})
    tags = html.find('li', {"class": "category"})
    text = ""
    for p in main.find_all('p', {'class': 'MsoNoSpacing'}):
        text = text + f' {p.text}'
    return {
        "url": url,
        "title": main.find('h1').text.strip(),
        "description": text.strip(),
        "tags": [tag.text for tag in tags.find_all('a') if tag.text.strip()],
        "site": site,
    }
