import os
import re
import mimetypes
from flask import render_template, redirect, url_for
from flask import send_file
from flask import request
from flask import Response
from app import app
# from app import lm
# from app import db, oid
from app import video_handler
from config import video_basedir


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
    lists = [l.split('/')[-1] for l in video_handler.find_lists(video_basedir)]
    return render_template('video.html', lists=lists)


@app.route('/video/<lst>')
def list_view(lst):
    lists = video_handler.find_lists(video_basedir)
    list_map = {l.split('/')[-1]: l for l in lists}

    if lst not in list_map:
        redirect(url_for('index'))
        return
    else:
        files = video_handler.list_files(list_map[lst])
        return render_template('list.html', files=files, list=lst)


@app.route('/video/<lst>/conv/<filename>')
def file_convert_view(lst, filename):
    filename = '.'.join(filename.split('.')[:-1])
    file_path = identify_file(lst, filename)
    if not file_path:
        redirect(url_for('index'))

    file_path = video_handler.convert_on_the_disk(file_path)
    if not file_path:
        redirect(url_for('index'))

    return send_file_partial(file_path)


@app.route('/video/<lst>/<filename>')
def file_view(lst, filename):
    if filename.endswith('.cnv'):
        return file_convert_view(lst, filename)
    file_path = identify_file(lst, filename)
    if not file_path:
        # FIXME - redirect needs to be returned
        redirect(url_for('index'))

    # return send_file(video_handler.get_file_contents(file_path),
    #                  mimetype='video/ogg')
    # return send_file(file_path, mimetype='video/ogg')
    return send_file_partial(file_path)


@app.route('/static/<fl>')
def statics(fl):
    return send_file('./static/' + fl)


def identify_file(lst, filename):
    lists = video_handler.find_lists(video_basedir)
    list_map = {l.split('/')[-1]: l for l in lists}

    if lst not in list_map:
        return None

    # files = video_handler.list_files(list_map[lst])
    res = [f for f in os.listdir(list_map[lst]) if f.startswith(filename)]
    if not res:
        return None
    file_path = os.path.join(list_map[lst], res[0])
    return file_path


@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def send_file_partial(path):
    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(path)

    size = os.path.getsize(path)
    byte1, byte2 = 0, None

    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()

    if g[0]:
        byte1 = int(g[0])
    if g[1]:
        byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1

    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data,
                  206,
                  mimetype=mimetypes.guess_type(path)[0],
                  direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'
                   .format(byte1, byte1 + length - 1, size))

    return rv
