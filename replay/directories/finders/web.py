from pyquery import PyQuery as PQ
import requests


def find(url):
    response = requests.get(url)
    if response.status_code != 200:
        return

    pq = PQ(response.content)
    for link in pq.find('link[rel="alternate"][href]'):
        link_type = link.get('type')
        if 'xml' in link_type:
            return link.get('href')
