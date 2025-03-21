from datetime import datetime

from flask import (
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer import app, get_db_connection
from page_analyzer.models.urls import URLRepository
from page_analyzer.utils import normalize_url
from validators.url import url as is_url

repo = URLRepository(get_db_connection)


@app.route('/')
def urls_index():
    return render_template(
        'index.html'
    )


@app.route('/urls')
def urls_get():
    urls = repo.list()

    return render_template(
        'list.html',
        urls=urls
    )


@app.route('/urls', methods=['POST'])
def urls_post():
    input_data = request.form.to_dict()
    url_name = input_data['url']

    errors = validate(url_name)

    if not errors:
        url_normalized = normalize_url(url_name)
        url_data = repo.find_by_name(url_normalized)

        if not url_data:
            url_data = {'name': url_normalized, 'created_at': datetime.now()}
            repo.save(url_data)
            flash('Страница успешно добавлена', 'success')
        else:
            flash('Страница уже существует', 'info')

        return redirect(url_for('urls_show', id=url_data['id']))

    return render_template(
        'index.html',
        url=url_name,
        errors=errors
    ), 422


@app.route('/urls/<id>')
def urls_show(id):
    url = repo.find(id)
    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'show.html',
        url=url,
        messages=messages
    )


def validate(url):
    errors = {}
    if not is_url(url) or len(url) > 255:
        errors['name'] = 'Некорректный URL'

    return errors
