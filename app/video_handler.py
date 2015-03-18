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


def list_files(listname):
    res = [{'file': '.'.join(f.split('.')[:-1]), 'ready': True}
           for f in os.listdir(listname)
           if any([f.endswith(t) for t in supported])]
    res.extend([{'file': '.'.join(f.split('.')[:-1])+'.cnv', 'ready':
                 os.path.exists(tmpfilename(os.path.join(listname, f)))}
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


def convert_on_the_disk(msg):
    tmpname = shlex.quote(tmpfilename(msg['file']))
    file = shlex.quote(msg['file'])
    msg['tmpname'] = tmpname

    # msg = {'f1': file, 'f2': tmpname}
    if msg not in queue:
        if not os.path.exists(tmpname):
            queue.put(msg)
        else:
            return tmpname


def get_file_contents(file):
    with open(file, 'rb') as f:
        return f.read()


def convert_on_the_fly(file):
    pass
    # with open(file, 'rb') as f:
    #     dmx = Demuxer(f)
    #     sid = find_stream(dmx.streams, 0, MediaType.AVMEDIA_TYPE_VIDEO)

    #     # vstream = dmx.streams[sid]
    #     vdec = dmx.open_decoder(sid)
    #     params = {
    #         'bit_rate': 800000,
    #         'width': 352,
    #         'height': 288,
    #         'pix_fmt': PixelFormat.AV_PIX_FMT_YUV420P,
    #     }
    #     res = io.BytesIO()
    #     res.name = 'out.ogv'
    #     mux = Muxer(res, name='ogv')
    #     venc = mux.open_encoder("libtheora", params)
    #     mux.write_header()

    #     while True:
    #         try:
    #             frame = vdec.decode(dmx.stream(sid))
    #             mux.write_frame(venc.encode(frame))
    #         except (pyrana.errors.NeedFeedError, pyrana.errors.EOSError):
    #             break

    #     mux.write_packet(venc.flush())
    #     # res.write(bytes(pkt[1]))
    #     mux.write_trailer()
    #     res.flush()
    #     return res


def identify_file(lst, filename, video_basedir=video_basedir):
    _, lists = find_lists(video_basedir)
    list_map = {l.split('/')[-1]: l for l in lists}

    if lst not in list_map:
        return None

    # files = video_handler.list_files(list_map[lst])
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
