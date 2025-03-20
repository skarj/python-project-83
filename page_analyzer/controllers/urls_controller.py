from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    get_flashed_messages
)
from datetime import datetime
from validators.url import url

from page_analyzer import app
from page_analyzer.models.urls import URLRepository
from page_analyzer import get_db_connection

repo = URLRepository(get_db_connection())


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
    data = request.form.to_dict()

    #  validation У URL обязательно должен быть валидный адрес,
    #  не превышающий 255 символов
    #  Для нормализации имени сайта используйте urlparse
    #  if exists
    errors = validate(data)

    if not errors:
        name = data['url']
        url = repo.find_by_name(name)

        if not url:
            url = {'name': data['url'], 'created_at': datetime.now()}
            repo.save(url)
            flash('Страница успешно добавлена', 'success')
        else:
            flash('Страница уже существует', 'info')

        return redirect(url_for('urls_show', id=url['id']))

    return render_template(
        'index.html',
        url=data.get('url'),
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


def validate(data):
    errors = {}
    if not url(data['url']):
        errors['name'] = 'Некорректный URL'

    return errors
