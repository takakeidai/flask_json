

from flask import (
    Blueprint, request, jsonify, abort
)

from flaskr.db import get_db

from flaskr import error_handling

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
    
    # まずPOSTされた形式がJSONかチェックする。
    if request.is_json:

        """
        res = request.get_json()の時点で400エラーが起きている。
        <title>400 Bad Request</title>
        <h1>Bad Request</h1>
        <p>Failed to decode JSON object: Expecting value: line 4 column 14 (char 17)</p>
        対処が必要
        <= この対処には、@bp.app_errorhandler(400)で400番台エラー用の関数を作成
        """
        res = request.get_json()
        
        # titleという情報があるかチェック、なければ400のエラー
        if "title" not in res.keys():
            message = "Title not found"
            status_code = 400
            return error_handling.response_error(message, status_code)
            
        # bodyという情報があるかチェック、なければ400のエラー
        if "body" not in res.keys():
            message = "body not found"
            status_code = 400
            return error_handling.response_error(message, status_code)

        # タイトルが空欄だと400番のエラー
        # JSONでは" "を送ってもNoneにはならずlenghtが0の文字列として認識される。
        if len(res['title']) == 0:
            message = "Title is required"
            status_code = 400
            return error_handling.response_error(message, status_code)
        
        
        title = res['title'] 
        body = res['body']

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
    
    
    # POSTされた形式がJSONでないならば、400のエラー  
    else:
        message = "data posted is not JSON"
        status_code = 400
        return error_handling.response_error(message, status_code)



# 引数に取ったidが存在するかどうかの判定をする関数
def isID(id):
    db = get_db()
    posts = db.execute(
        'SELECT id, title, body, created'
        ' FROM post'
        ' ORDER BY created DESC'
    ).fetchall()
    
    post_id_list = []
    for post in posts:
        post_id_list.append(post['id'])
    
    if id in post_id_list:
        return True
    else:
        return False



@bp.route('/blog/<int:id>', methods = ['GET'])
def get_post_by_id(id):

    # URLで指定されたidが存在しないなら404番のエラー
    if not isID(id):
        abort(404)   
    
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
    
    # URLで指定されたidが存在しないなら404番のエラー
    if not isID(id):
        abort(404)
    
    # putされた情報がJSONかチェック
    if request.is_json:
        res = request.get_json()
        
        if "title" not in res.keys():
            message = "Title not found"
            status_code = 400
            return error_handling.response_error(message, status_code)
        
        if "body" not in res.keys():
            message = "body not found"
            status_code = 400
            return error_handling.response_error(message, status_code)

        if len(res['title']) == 0:
            message = "Title is required"
            status_code = 400
            return error_handling.response_error(message, status_code)
        
        title = res['title'] 
        body = res['body']
        
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
        
    else:
        message = "data posted is not JSON"
        status_code = 400
        return error_handling.response_error(message, status_code)
    


@bp.route('/blog/<int:id>', methods = ['DELETE'])
def delete(id):
    
    # URLで指定されたidが存在しないなら404番のエラー
    if not isID(id):
        abort(404)
        
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    message = {
        "message" : "your post is deleted."
    }
    return jsonify(message)



