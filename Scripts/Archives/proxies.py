"""
Henry Manley - hjm67@cornell.edu -  Last Modified 6/7/2021
"""

import requests
from lxml.html import fromstring
import random

def get_proxies():
    """
    Return a list of free HTTPS proxies.
    """

    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)

    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            addProxy = 'https://' + proxy
            proxies.add(addProxy)
            addProxy = 'http://' + proxy
            proxies.add(addProxy)
    proxies = list(proxies)
    proxies = random.sample(proxies, len(proxies))
    return proxies
