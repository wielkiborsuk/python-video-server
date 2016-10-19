import os
# import subprocess
import shlex
import hashlib
import threading
from app.background_processor import UniqueQueue
from app.background_processor import process_videos
from config import video_basedir

# pyrana.setup()
supported = ['mp4']
convertable = ['avi', 'mkv', 'ogg', 'wmv', 'mpeg', 'mpg']
queue = UniqueQueue()
worker = threading.Thread(target=process_videos, args=(queue,))
worker.setDaemon(True)
worker.start()


def find_lists(basedir=video_basedir):
    lists = []
    for b, dirs, files in os.walk(basedir):
        flag = any([any([f.endswith(t) for t in (supported + convertable)])
                    for f in files])
        if flag:
            lists.append(b)

    courses = []
    for b, dirs, files in os.walk(basedir):
        if 'course.md' in files:
            for d in dirs:
                try:
                    pass
                    # lists.remove(os.path.join(b, d))
                except Exception:
                    pass
            courses.append(b)
    return courses, lists



def is_pending(file_path):
    return get_msg_for_file(file_path) in queue


def is_ready(file_path):
    return (os.path.exists(tmpfilename(file_path)) and
            not is_pending(file_path))


def list_files(listname):
    res = [{'file': '.'.join(f.split('.')[:-1]), 'ready': True}
           for f in os.listdir(listname)
           if any([f.endswith(t) for t in supported])]
    res.extend([{'file': '.'.join(f.split('.')[:-1])+'.cnv', 'ready':
                 is_ready(os.path.join(listname, f))}
                for f in os.listdir(listname)
                if any([f.endswith(t) for t in convertable])])
    res.sort(key=lambda el: el['file'])

    return res


def list_course(course):
    _, lists = find_lists(course)
    lists.sort()
    res = [{'name': l.split('/')[-1], 'path':l, 'files': list_files(l)}
           for l in lists]

    return res


def tmpfilename(file):
    return '/tmp/{}.mp4'.format(hashlib.md5(file.encode()).hexdigest())


def get_msg_for_file(file_path):
    tmpname = shlex.quote(tmpfilename(file_path))
    return {'file': file_path, 'tmpname': tmpname}


def convert_on_the_disk(file_path):
    if not is_ready(file_path) and not is_pending(file_path):
        queue.put(get_msg_for_file(file_path))
    return tmpfilename(file_path)


def check_status(file_path):
    return {'ready': is_ready(file_path),
            'pending': is_pending(file_path)}


def identify_file(lst, filename, video_basedir=video_basedir):
    _, lists = find_lists(video_basedir)
    list_map = {l.split('/')[-1]: l for l in lists}

    if lst not in list_map:
        return None

    res = [f for f in os.listdir(list_map[lst]) if f.startswith(filename)]
    if not res:
        return None
    file_path = os.path.join(list_map[lst], res[0])
    return file_path


if __name__ == '__main__':
    lists = find_lists('/home/borsuk/video')
    print(lists)
    for l in lists:
        print(list_files(l))
