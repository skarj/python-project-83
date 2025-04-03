import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    get_flashed_messages,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer import db
from page_analyzer.clients import http
from page_analyzer.parsers import html
from validators.url import url as is_url

from .models import URL, URLCheck

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')


@app.route('/')
def urls_index():
    return render_template(
        'index.html'
    )


@app.route('/urls')
def urls_get():
    with db.connection(DATABASE_URL) as conn:
        all_urls: list[URL] = db.get_all_urls(conn)
        latest_url_checks: dict[int, URLCheck] = {
            c.url_id: c for c in sorted(
                db.get_all_checks(conn),
                key=lambda x: (x.id, x.created_at)
            )
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
    url_name = input_data.get('url')

    if not url_name:
        return jsonify({"error": "URL name cannot be empty"}), 400

    errors = validate_url(url_name)
    if errors:
        return render_template(
            'index.html',
            url=url_name,
            errors=errors
        ), 422

    url_normalized = normalize_url(url_name)
    with db.connection(DATABASE_URL) as conn:
        url = db.get_url_by_name(conn, url_normalized)

        if not url:
            url = URL(name=url_normalized)
            db.create_url(conn, url)

            flash('Страница успешно добавлена', 'success')
        else:
            flash('Страница уже существует', 'info')

    return redirect(url_for('urls_show', id=url.id))


@app.route('/urls/<int:id>')
def urls_show(id):
    with db.connection(DATABASE_URL) as conn:
        url = get_url_or_404(conn, id)
        url_checks = db.get_checks_for_url(conn, url.id)

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show.html',
        url=url,
        checks=url_checks,
        messages=messages
    )


@app.route('/urls/<id>/checks', methods=['POST'])
def checks_post(id):
    with db.connection(DATABASE_URL) as conn:
        url = get_url_or_404(conn, id)

    response = http.get(url.name)

    if response:
        h1, title, description = html.get_seo_content(response.content)

        url_check = URLCheck(
            url_id=url.id,
            h1=h1,
            title=title,
            description=description,
            status_code=response.status_code
        )

        with db.connection(DATABASE_URL) as conn:
            db.create_url_check(conn, url_check)

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


def get_url_or_404(conn, id):
    url = db.get_url_by_id(conn, id)

    if not url:
        abort(404)

    return url
