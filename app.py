# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from math import ceil

import config

app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False  # Last slash problem
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/')
def default():
    return 'Используйте локацию /items'


@app.route('/items', methods=['GET', 'POST', 'PUT'])
def index():
    from models import GuestBook
    from forms import GuestBookForm

    page_num = request.args.get('page', default=0, type=int)
    items_count_in_page = request.args.get('per_page', default=5, type=int)
    if items_count_in_page > 10: items_count_in_page = 3  # LoL

    if request.method == 'GET':
        guestbooks = GuestBook.query.limit(items_count_in_page).offset(page_num * items_count_in_page).all()

        resp = make_response(jsonify(dict(Guestbook=[p.to_json() for p in guestbooks])))
        resp.headers['X-Total-Count'] = GuestBook.query.count()
        link_header = \
            '<{}?page={}&per_page={}>; rel="next",\
            <{}?page={}&per_page={}>; rel="last"' \
            .format(request.base_url, page_num + 1, items_count_in_page,
                    request.base_url, ceil(int(resp.headers['X-Total-Count']) / items_count_in_page),
                    items_count_in_page)

        resp.headers['Link'] = link_header
        return resp

    if request.method == 'POST':
        form = GuestBookForm(request.form)
        if form.validate():
            post = GuestBook(**form.data)
            db.session.add(post)
            db.session.commit()
            resp = make_response(edit_post(post.id))
            resp.headers['Location'] = '/items/{}'.format(post.id)

            return resp, 201
        else:

            return 'Post NOT created! {}'.format(str(form.errors))

    if request.method == 'PUT':
        if not request.form:
            db.session.query(GuestBook).delete()
            db.session.commit()

            return 'Guestbook cleared!'
        else:

            return 'Запрос не обработан, PUT не пустой'


@app.route('/items/<int:post_id>', methods=['PATCH', 'PUT', 'GET', 'DELETE'])
def edit_post(post_id):
    if request.method in ['PATCH', 'PUT']:
        try:
            q = GuestBook.query.get(int(post_id))
            if request.form.get('author'):
                q.author = request.form.get('author')
            if request.form.get('mess_txt'):
                q.mess_txt = request.form.get('mess_txt')
            # q.date_updated = datetime.utcnow()
            db.session.commit()

            return jsonify({'Post edited': [q.to_json()], })
        except:

            return 'Post ID out of range or invalid arguments taken', 404

    if request.method == 'DELETE':
        try:
            q = GuestBook.query.get(int(post_id))
            q.del_flag = True
            return 'Post mark as deleted', 200
        except:
            return '', 204

    try:
        q = GuestBook.query.filter(GuestBook.id == int(post_id))[0]

        return jsonify({'Post': [q.to_json()], })
    except:
        return 'Post ID out of range', 403


if __name__ == '__main__':
    from models import *

    db.create_all()

    # Running app:
    app.run('0.0.0.0')
