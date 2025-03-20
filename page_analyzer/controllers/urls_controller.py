from flask import request, render_template, flash, redirect, url_for
from datetime import datetime

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

    url = {'name': data['url'], 'created_at': datetime.now()}

    repo.save(url)
    flash('URL was added successfully', 'success')

    return redirect(url_for('urls_index'))


@app.route('/urls/<id>')
def urls_show(id):
    url = repo.find(id)

    return render_template(
        'show.html',
        url=url,
    )
