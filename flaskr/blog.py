

from flask import (
    Blueprint, flash, g, request, jsonify
)

from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/blog', methods = ['GET'])
def get_posts():
    db = get_db()
    posts = db.execute(
        'SELECT id, title, body, created'
        ' FROM post'
        ' ORDER BY created DESC'
    ).fetchall()
    
    posts_list = []
    for post in posts:
        posts_list.append(
            dict(
                id = post['id'],
                title = post["title"],
                body = post["body"],
                created_at = post["created"]
                )
            )
        
    return jsonify(posts_list)


@bp.route('/blog', methods = ['POST'])
def create():
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
         


@bp.route('/blog/<int:id>', methods = ['GET'])
def get_post_by_id(id):
    db = get_db()
    post = get_db().execute(
        'SELECT id, title, body, created'
        ' FROM post'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    
    post_contents = []
    post_contents.append(
        dict(
            id = id,
            title = post["title"],
            body = post["body"],
            created_at = post["created"]
            )
        )
    print(post_contents)
        
    return jsonify(post_contents)



@bp.route('/blog/<int:id>', methods = ['PUT'])
def update(id):
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
    
    

@bp.route('/blog/<int:id>', methods = ['DELETE'])
def delete(id):
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    message = {
        "message" : "your post is deleted."
    }
    return jsonify(message)