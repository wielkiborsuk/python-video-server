import os
import re
import mimetypes
import json
# import time
from functools import partial
from flask import render_template, redirect
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
@app.route('/video')
def lists():
    lists = [l.split('/')[-1] for l in
             video_handler.find_lists(video_basedir)[1]]

    courses = [c.split('/')[-1] for c in
               video_handler.find_lists(video_basedir)[0]]

    return render_template('video.html', lists=lists, courses=courses)


@app.route('/video/course/<course>')
def course_view(course):
    courses, _ = video_handler.find_lists(video_basedir)
    course_map = {c.split('/')[-1]: c for c in courses}

    if course not in course_map:
        return redirect('index')
    else:
        return render_template('course.html', course=course)


@app.route('/video/course/<course>/lists')
def course_lists_json(course):
    courses, _ = video_handler.find_lists(video_basedir)
    course_map = {c.split('/')[-1]: c for c in courses}

    lists = video_handler.list_course(course_map[course])
    return json.dumps(lists)


@app.route('/video/<lst>')
def list_view(lst):
    _, lists = video_handler.find_lists(video_basedir)
    list_map = {l.split('/')[-1]: l for l in lists}

    if lst not in list_map:
        return redirect('index')
    else:
        files = video_handler.list_files(list_map[lst])
        return render_template('list.html', files=json.dumps(files), list=lst)


@app.route('/video/<lst>/conv/<filename>')
def file_convert_view(lst, filename):
    filename = '.'.join(filename.split('.')[:-1])
    file_path = video_handler.identify_file(lst, filename, video_basedir)
    if not file_path:
        redirect('index')

    file_path = video_handler.tmpfilename(file_path)
    if not file_path:
        redirect('index')

    return send_file_partial(file_path)


@app.route('/video/request/<lst>/<filename>/status')
def check_status(lst, filename):
    filename = '.'.join(filename.split('.')[:-1])
    file_path = video_handler.identify_file(lst, filename, video_basedir)

    return json.dumps(video_handler.check_status(file_path))


@app.route('/video/request/<lst>/<filename>')
def request_video(lst, filename):
    filename = '.'.join(filename.split('.')[:-1])
    file_path = video_handler.identify_file(lst, filename, video_basedir)

    tmpfile = video_handler.convert_on_the_disk(file_path)

    return json.dumps({"status": 200, "tmpfile": tmpfile})


@app.route('/video/<lst>/<filename>')
def file_view(lst, filename):
    if filename.endswith('.cnv'):
        return file_convert_view(lst, filename)
    file_path = video_handler.identify_file(lst, filename, video_basedir)
    if not file_path:
        # FIXME - redirect needs to be returned
        redirect('index')

    return send_file_partial(file_path)


@app.route('/static/<fl>')
def statics(fl):
    return send_file('./static/' + fl)


@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def send_file_partial(path):
    range_header = request.headers.get('Range', None)

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
        length = byte2 - byte1 + 1

    def generate():
        chunksize = 1024 * 1024
        with open(path, 'rb') as f:
            f.seek(byte1)
            count = 0
            for chunk in iter(partial(f.read, chunksize), ''):
                chunk = (chunk[:(length-count)]
                         if length < count + chunksize else chunk)
                count += chunksize
                yield chunk
                if count > length:
                    return

    rv = Response(generate(),
                  206,
                  mimetype=mimetypes.guess_type(path)[0],
                  direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'
                   .format(byte1, byte1 + length - 1, size))

    return rv
