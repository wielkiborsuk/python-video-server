import os
import io
import pyrana
from pyrana.formats import find_stream, MediaType
from pyrana.video import PixelFormat

pyrana.setup()


def find_lists(basedir='.'):
    res = []
    for b, dirs, files in os.walk(basedir):
        flag = False
        for f in files:
            if f.endswith('avi') or f.endswith('mp4'):
                flag = True
        if flag:
            res.append(b)
    return res


def list_files(listname):
    res = ['.'.join(f.split('.')[:-1]) for f in os.listdir(listname)
           if f.endswith('avi') or f.endswith('mp4')]
    return res


def get_file_contents(file):
    with open(file, 'rb') as f:
        dmx = pyrana.Demuxer(f)
        sid = find_stream(dmx.streams, 0, MediaType.AVMEDIA_TYPE_VIDEO)

        # vstream = dmx.streams[sid]
        vdec = dmx.open_decoder(sid)
        params = {
            'bit_rate': 800000,
            'width': 352,
            'height': 288,
            'time_base': (1, 25),
            'pix_fmt': PixelFormat.AV_PIX_FMT_YUV420P,
        }
        venc = pyrana.video.Encoder("libx264", params)
        res = io.BytesIO()

        while True:
            frame = vdec.decode(dmx.stream(sid))
            try:
                pkt = venc.encode(frame)
                res.write(bytes(pkt))
            except pyrana.errors.NeedFeedError:
                pass

        res.writes(bytes(venc.flush()))
        return res


if __name__ == '__main__':
    lists = find_lists('/home/borsuk/video')
    print(lists)
    for l in lists:
        print(list_files(l))
