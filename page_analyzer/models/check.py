from psycopg2.extras import DictCursor


class CheckRepository:
    def __init__(self, conn):
        self.conn = conn

    def list_by_url_id(self, url_id):
        with self.conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                    SELECT *
                    FROM url_checks
                    WHERE url_id = %s
                    ''', (url_id,))
                return [dict(row) for row in cur]

    def save(self, check):
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
