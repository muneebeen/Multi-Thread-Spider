import urllib.parse
from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.links = set()

    def handle_starttag(self, tag: str, attrs):
        if tag == 'a':
            for (attr, value) in attrs:
                if attr == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message: str) -> (): pass

