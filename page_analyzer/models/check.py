import requests
from bs4 import BeautifulSoup
from psycopg2.extras import DictCursor


class CheckRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_all_by_url_id(self, url_id):
        with self.conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                    SELECT *
                    FROM url_checks
                    WHERE url_id = %s
                    ''', (url_id,))
                return [dict(row) for row in cur]

    def create(self, check):
        with self.conn() as conn:
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
                        check['url_id'],
                        check['status_code'],
                        check['h1'],
                        check['title'],
                        check['description'],
                        check['created_at'],
                    )
                )
                check_id = cur.fetchone()[0]
                check['id'] = check_id

            conn.commit()


class Check:
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
