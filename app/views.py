from flask import render_template, flash, redirect, session, url_for, request, g
from app import app
from app import lm
from app import db, oid
from app import video_handler

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'wielki.borsuk', 'email': 'wielki.borsuk@gmail.com'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/video')
def lists():
    lists = [l.split('/')[-1] for l in video_handler.find_lists('/home/borsuk/video')]
    return render_template('video.html', lists=lists)

@app.route('/video/<list>')
def list(lst):
    lists = video_handler.find_lists('/home/borsuk/video')
    list_map = {l.split('/')[-1]: l for l in lists}

    if lst not in list_map:
        redirect(url_for('index'))
        return
    else:
        files = video_handler.list_files(list_map[lst])
        return render_template('list.html', files=files)

