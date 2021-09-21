import sqlite3
import random, string
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.exceptions import abort

rnd = random.SystemRandom()

app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(rnd.choice(string.ascii_letters) for i in range(666))

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
  conn = get_db_connection()
  post_u = conn.execute('SELECT * FROM posts WHERE id=(SELECT MAX(id) FROM posts)').fetchall()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  conn.close()
  return render_template('index.html', post_u=post_u, posts=posts)

@app.route('/admin', methods=('GET','POST'))
def admin():
  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']

    if not title:
        flash('Title is required!')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO posts(title, content) VALUES (?,?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
  conn.close()

  return render_template('admin.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/<int:id>/edit', methods=('PUT'))
def edit(id):
  post = get_post(id)

  title = request.form['title']
  content = request.form['content']

  conn = get_db_connection()
  conn.execute('UPDATE posts SET title = ?, content =?'
                   ' WHERE id = ?', (title, content, id))
  conn.commit()
  conn.close()
  #return redirect(url_for('admin'))
  return render_template('edit.html', post=post)

@app.route('/<int:id>/delete')
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('admin'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
