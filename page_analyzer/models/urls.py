from psycopg2.extras import DictCursor


class URLRepository:
    def __init__(self, conn):
        self.conn = conn

    def list(self):
        with self.conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                    SELECT *,
                        (SELECT created_at
                            FROM url_checks
                            WHERE url_id = url.id
                            ORDER BY id DESC
                            LIMIT 1) AS last_check
                    FROM urls AS url
                    ''')
                return [dict(row) for row in cur]

    def save(self, url):
        if 'id' in url and url['id']:
            self._update(url)
        else:
            self._create(url)

    def find_by_name(self, name):
        with self.conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
                row = cur.fetchone()
                return dict(row) if row else None

    def _update(self, url):
        with self.conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE urls SET name = %s, created_at = %s WHERE id = %s',
                    (url['name'], url['created_at'], url['id'])
                )

            conn.commit()

    def find(self, id):
        with self.conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def _create(self, url):
        with self.conn() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s)
                    RETURNING id
                    ''', (url['name'], url['created_at'])
                )
                url_id = cur.fetchone()[0]
                url['id'] = url_id

            conn.commit()
        #  https://github.com/hexlet-components/python-flask-example/blob/database/user_repository.py#L41
