import urllib.request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def download_page(url: str) -> object:
    try:
        ua = UserAgent(browsers=['edge', 'chrome'])
        agent = ua.random
        headers = {"User-Agent": agent}
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        resp_data = str(resp.read())
        return BeautifulSoup(resp_data, "html.parser")
    except Exception as e:
        print(str(e))
        return BeautifulSoup(None, "html.parser")
