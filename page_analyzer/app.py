import os
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.db import (
    URL,
    Response,
    URLCheck,
    create_url,
    create_url_check,
    get_all_checks,
    get_all_urls,
    get_checks_for_url,
    get_url_by_id,
    get_url_by_name,
)
from validators.url import url as is_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')


def connection(db_url):
    return psycopg2.connect(db_url)


@app.route('/')
def urls_index():
    return render_template(
        'index.html'
    )


@app.route('/urls')
def urls_get():
    with connection(DATABASE_URL) as conn:
        all_urls: list[URL] = get_all_urls(conn)
        latest_url_checks: dict[int, URLCheck] = {
            c.url_id: c for c in sorted(get_all_checks(conn), key=lambda x: (x.id, x.created_at))
        }

    return render_template(
        'list.html',
        urls=[
            {
                'url': url,
                'url_check': latest_url_checks.get(url.id),
            }
            for url in all_urls
        ]
    )


@app.route('/urls', methods=['POST'])
def urls_post():
    input_data = request.form.to_dict()
    url_name = input_data['url']
    errors = validate_url(url_name)

    if not errors:
        url_normalized = normalize_url(url_name)
        with connection(DATABASE_URL) as conn:
            url = get_url_by_name(conn, url_normalized)

        if not url:
            url = URL(
                name=url_normalized,
                created_at=datetime.now()
            )
            with connection(DATABASE_URL) as conn:
                create_url(conn, url)

            flash('Страница успешно добавлена', 'success')
        else:
            flash('Страница уже существует', 'info')

        return redirect(url_for('urls_show', id=url.id))

    return render_template(
        'index.html',
        url=url_name,
        errors=errors
    ), 422


@app.route('/urls/<id>')
def urls_show(id):
    with connection(DATABASE_URL) as conn:
        url = get_url_by_id(conn, id)
        url_checks = get_checks_for_url(conn, url.id)

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show.html',
        url=url,
        checks=url_checks,
        messages=messages
    )


@app.route('/urls/<id>/checks', methods=['POST'])
def checks_post(id):
    with connection(DATABASE_URL) as conn:
        url = get_url_by_id(conn, id)

    response = get_response(url.name)

    if response:
        h1, title, description = get_seo_content(response.content)

        url_check = URLCheck(
            url_id=url.id,
            h1=h1,
            title=title,
            description=description,
            status_code=response.status_code,
            created_at=datetime.now()
        )

        with connection(DATABASE_URL) as conn:
            create_url_check(conn, url_check)

        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('urls_show', id=id))


def validate_url(url):
    errors = {}
    if not is_url(url) or len(url) > 255:
        errors['name'] = 'Некорректный URL'

    return errors


def normalize_url(url):
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    return f"{scheme}://{netloc}"


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
