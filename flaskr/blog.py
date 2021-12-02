

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from werkzeug.security import check_password_hash

from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/blog', methods = ('GET','POST'))
def index_and_create():
    if request.method == 'POST':
        res = request.get_json()
        title = res['title']
        body = res['body']
        error = None
        
        if not title:
            error = 'Title is required.'
            
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body)'
                ' VALUES (?, ?)',
                (title, body)
            )
            db.commit()
            message = {
                "message" : "new post is successfully created."
            }
            return jsonify(message)
        
    db = get_db()
    posts = db.execute(
        'SELECT id, title, body, created'
        ' FROM post'
        ' ORDER BY created DESC'
    ).fetchall()
    
    posts_list_without_index = []
    for post in posts:
        posts_list_without_index.append(
            dict(
                id = post['id'],
                title = post["title"],
                body = post["body"],
                created_at = post["created"]
                )
            )
        
    return jsonify(posts_list_without_index)
        



@bp.route('/blog/<int:id>', methods = ('GET', 'PUT', 'DELETE'))
def update_and_delete(id):
    
    if request.method == 'PUT':
        res = request.get_json()
        title = res['title']
        body = res['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            message = {
                "message" : "your post is updated."
            }
            return jsonify(message)
    
    if request.method == 'DELETE':
        db = get_db()
        db.execute('DELETE FROM post WHERE id = ?', (id,))
        db.commit()
        message = {
            "message" : "your post is deleted."
        }
        return jsonify(message)
    
    return redirect(url_for('blog.index'))


