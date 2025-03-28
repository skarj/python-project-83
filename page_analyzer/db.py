import dataclasses
from datetime import datetime

from psycopg2.extras import DictCursor


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


def get_all_urls(conn):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT * FROM urls')
        return [URL(**row) for row in cur]


def get_url_by_name(conn, name):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s', (name,))
        row = cur.fetchone()
        return URL(**row) if row else None


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
        row = cur.fetchone()
        return URL(**row) if row else None


def get_checks_for_url(conn, url_id):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('''
            SELECT *
            FROM url_checks
            WHERE url_id = %s
        ''', (url_id,))
        row = cur.fetchone()
        return [URLCheck(**row) for row in cur]


def get_all_checks(conn):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT * FROM url_checks')
        return [URLCheck(**row) for row in cur]


def create_url(conn, url):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s)
            RETURNING id
            ''', (url.name, url.created_at)
        )
        url_id = cur.fetchone()[0]
        url.id = url_id

    conn.commit()


def create_url_check(conn, url_check):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            ''', (
                url_check.url_id,
                url_check.status_code,
                url_check.h1,
                url_check.title,
                url_check.description,
                url_check.created_at,
            )
        )
        check_id = cur.fetchone()[0]
        url_check.id = check_id

    conn.commit()
