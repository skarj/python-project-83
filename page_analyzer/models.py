import dataclasses
from datetime import datetime


@dataclasses.dataclass
class URLCheck:
    url_id: int
    status_code: int
    h1: str
    title: str
    description: str
    created_at: datetime
    id: int | None = None


@dataclasses.dataclass
class URL:
    name: str
    created_at: datetime
    id: int | None = None


@dataclasses.dataclass
class Response:
    status_code: str
    content: str
