import requests
from bs4 import BeautifulSoup


class Site:
    def __init__(self, url):
        self.url = url
        self.status_code = None
        self.content = None

    def run_check(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.status_code = response.status_code
            self.content = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException:
            pass

    def get_h1(self):
        if self.content.h1:
            return self.content.h1.string
        return None

    def get_title(self):
        if self.content.title:
            return self.content.title.string
        return None

    def get_description(self):
        meta_description = self.content.find(
            "meta", attrs={"name": "description"}
        )

        if meta_description:
            return meta_description['content']
        return None
