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
from page_analyzer.models.check import CheckRepository
from page_analyzer.models.site import Site
from page_analyzer.models.url import URLRepository
from page_analyzer.utils import normalize_url
from validators.url import url as is_url

url_repo = URLRepository(get_db_connection)
check_repo = CheckRepository(get_db_connection)


@app.route('/')
def urls_index():
    return render_template(
        'index.html'
    )


@app.route('/urls')
def urls_get():
    urls = url_repo.list()

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
        url_data = url_repo.find_by_name(url_normalized)

        if not url_data:
            url_data = {'name': url_normalized, 'created_at': datetime.now()}
            url_repo.save(url_data)
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
    url_data = url_repo.find(id)
    messages = get_flashed_messages(with_categories=True)
    url_checks = check_repo.list_by_url_id(id)

    return render_template(
        'show.html',
        url=url_data,
        checks=url_checks,
        messages=messages
    )


@app.route('/urls/<id>/checks', methods=['POST'])
def checks_post(id):
    url_data = url_repo.find(id)
    site = Site(url_data['name'])
    site.run_check()

    if site.status_code:
        h1 = site.get_h1()
        title = site.get_title()
        description = site.get_description()
        check_data = {
            'url_id': id,
            'status_code': site.status_code,
            'h1': h1,
            'title': title,
            'description': description,
            'created_at': datetime.now()
        }
        print(check_data)
        check_repo.save(check_data)
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('urls_show', id=id))


def validate(url):
    errors = {}
    if not is_url(url) or len(url) > 255:
        errors['name'] = 'Некорректный URL'

    return errors
