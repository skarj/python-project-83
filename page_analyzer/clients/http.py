from dataclasses import dataclass

import requests


@dataclass
class Response:
    status_code: str
    content: str


def get(url_name, logger):
    try:
        resp = requests.get(url_name, timeout=10)
        resp.raise_for_status()
        return Response(
            content=resp.content,
            status_code=resp.status_code
        )
    except requests.RequestException as e:
        logger.error(f"Error getting url: {str(e)}")

    return None
