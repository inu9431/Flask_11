from flask import request, jsonify, render_template
from flask_smorest import Blueprint, abort


def create_posts_blueprint(mysql):
    posts_blp = Blueprint(
        "posts",
        __name__,
        description = "posts api",
        url_prefix="/posts",
    )

    @posts_blp.route('/', methods=['GET', 'POST'])
    def posts():
        cursor = mysql.connection.cursor()

        if request.method == 'GET':
            sql = 'SELECT * FROM posts'
            cursor.execute(sql)
            posts = cursor.fetchall()
            cursor.close()

            if request.accept_mimetypes.best_match(['application/json', 'text/html']) == 'text/html':
                post_list = [{'id': post[0], 'title':post[1], 'content': post[2]} for post in posts]
                return render_template('posts.html', posts=post_list)
            
            return jsonify([{'id': post[0], 'title': post[1], 'content': post[2]} for post in posts])
        
        if request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')
    
            if not title or not content:
                abort(400, message='title 또는 content가 없습니다')

            sql = 'INSERT INTO posts(title, content) VALUES(%s, %s)'
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({'message': 'successfully created post data', 'title':title, 'content': content}), 201
        

    @posts_blp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def post(id):
        cursor = mysql.connection.cursor()

    
        if request.method == 'GET':
            sql = f'SELECT * FROM posts WHERE id={id}'
            cursor.execute(sql)
            post = cursor.fetchone()
            cursor.close()

            if not post:
                abort(404, message="해당 게시글이 없습니다")

            return ({
                'id': post[0],
                'title': post[1],
                'content': post[2]
                })

        
        elif request.method == 'PUT':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content or not post:
                abort(400, message='title 또는 content가 없습니다')

            sql = f'UPDATE posts SET title={title}, content={content} WHERE id={id}'
            cursor.execute(sql)
            mysql = mysql.connection.commit()

            return jsonify({"msg": "successfully updated title & content"})
            

        elif request.method == 'DELETE':
            if not post:
                abort(400, "Not found post")
            sql = f'DELETE FROM posts WHERE id={id}'
            cursor.execute(sql)
            mysql.connention.commit()

            return jsonify({"msg": "successfully deleted title & content"})
            
    return posts_blp
