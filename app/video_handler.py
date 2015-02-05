import os
import sys
# import pyrana
import datetime
import subprocess
import shlex
# from pyrana.formats import find_stream, MediaType, Demuxer, Muxer
# from pyrana.video import PixelFormat
# from app.conv import process_file

# pyrana.setup()
supported = ['mp4', 'mpeg', 'mpg']
convertable = ['avi', 'mkv', 'ogg', 'wmv']


def find_lists(basedir='.'):
    res = []
    for b, dirs, files in os.walk(basedir):
        flag = any([any([f.endswith(t) for t in (supported + convertable)])
                    for f in files])
        if flag:
            res.append(b)
    return res


def list_files(listname):
    # res = [f for f in os.listdir(listname)
    #        if any([f.endswith(t) for t in supported])]
    res = ['.'.join(f.split('.')[:-1]) for f in os.listdir(listname)
           if any([f.endswith(t) for t in supported])]
    res.extend(['.'.join(f.split('.')[:-1])+'.cnv' for f in os.listdir(listname)
                if any([f.endswith(t) for t in convertable])])
    res.sort()

    return res


def convert_on_the_disk(file):
    file = shlex.quote(file)
    print(file)
    tmpname = '/tmp/' + str(datetime.datetime.now().timestamp()) + '.mp4'
    try:
        cmd = 'avconv -i {} -t 00:00:10 -strict experimental {}'.format(file, tmpname)
        subprocess.call(cmd, shell=True)
        return tmpname
    except Exception as e:
        print(e)
        sys.stderr.write("%s\n" % e)


def get_file_contents(file):
    with open(file, 'rb') as f:
        return f.read()


# def convert_on_the_fly(file):
#     with open(file, 'rb') as f:
#         dmx = Demuxer(f)
#         sid = find_stream(dmx.streams, 0, MediaType.AVMEDIA_TYPE_VIDEO)

#         # vstream = dmx.streams[sid]
#         vdec = dmx.open_decoder(sid)
#         params = {
#             'bit_rate': 800000,
#             'width': 352,
#             'height': 288,
#             'pix_fmt': PixelFormat.AV_PIX_FMT_YUV420P,
#         }
#         res = io.BytesIO()
#         res.name = 'out.ogv'
#         mux = Muxer(res, name='ogv')
#         venc = mux.open_encoder("libtheora", params)
#         mux.write_header()

#         while True:
#             try:
#                 frame = vdec.decode(dmx.stream(sid))
#                 mux.write_frame(venc.encode(frame))
#             except (pyrana.errors.NeedFeedError, pyrana.errors.EOSError):
#                 break

#         mux.write_packet(venc.flush())
#         # res.write(bytes(pkt[1]))
#         mux.write_trailer()
#         res.flush()
#         return res


if __name__ == '__main__':
    lists = find_lists('/home/borsuk/video')
    print(lists)
    for l in lists:
        print(list_files(l))
