"""
Utils methods for crawlers.
"""
import requests
from bs4 import BeautifulSoup

def get_html_from_url(url):
    """
    Retorna el html desde una url.

    url -- string.
    """
    page = requests.get(url)
    return BeautifulSoup(page.content, 'lxml')
