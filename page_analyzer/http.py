from .models import Response
from bs4 import BeautifulSoup
import requests


def get_seo_content(content):
    content = BeautifulSoup(content, 'html.parser')

    meta_description = content.find(
        "meta", attrs={"name": "description"}
    )

    return (
        content.h1.string if content.h1 else None,
        content.title.string if content.title else None,
        meta_description['content'] if meta_description else None,
    )


def get_response(url_name):
    try:
        resp = requests.get(url_name)
        resp.raise_for_status()
        return Response(
            content=resp.content,
            status_code=resp.status_code
        )
    except requests.exceptions.RequestException:
        pass

    return None
