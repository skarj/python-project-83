from urllib.parse import urlparse


def normalize_url(url):
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    return f"{scheme}://{netloc}"
