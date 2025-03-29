import requests

from ..models import Response


def get_response(url_name):
    try:
        resp = requests.get(url_name, timeout=10)
        resp.raise_for_status()
        return Response(
            content=resp.content,
            status_code=resp.status_code
        )
    except requests.RequestException:
        pass

    return None
