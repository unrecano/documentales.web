"""
Utils methods for crawlers.
"""
import random
import requests
from bs4 import BeautifulSoup

def get_html_from_url(url, random_agent=False):
    """
    Retorna el html desde una url.

    url -- string.
    """
    headers = {"user-agent": get_user_agent()} if random_agent else {}
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, 'lxml')

def get_user_agent():
    """
    Choice a random user agent from a remote file.
    """
    url = "https://gitlab.com/-/snippets/2087548/raw/master/snippetfile1.txt"
    content = requests.get(url).content.decode("utf-8")
    user_agents = content.split("\n")[:-1]
    return random.choice(user_agents)
