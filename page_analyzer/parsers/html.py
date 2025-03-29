from bs4 import BeautifulSoup


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
