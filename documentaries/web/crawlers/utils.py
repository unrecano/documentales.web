"""
Utils methods for crawlers.
"""
import random
from urllib import request
import requests
from bs4 import BeautifulSoup

def get_html_from_url(url):
    """
    Retorna el html desde una url.

    url -- string.
    """
    headers = {"user-agent": get_user_agent()}
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, 'lxml')

def get_user_agent():
    url = "https://gitlab.com/-/snippets/2087548/raw/master/snippetfile1.txt"
    content = requests.get(url).content.decode("utf-8")
    ua = content.split("\n")[:-1]
    return random.choice(ua)
