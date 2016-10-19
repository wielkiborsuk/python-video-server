import os
import queue
import shlex
import subprocess
from timeit import default_timer as timer


class UniqueQueue(queue.Queue):
    """Docstring for UniqueQueue. """

    def _init(self, maxsize):
        super()._init(maxsize)
        self.history = []

    def _put(self, el):
        if el not in self.history:
            super()._put(el)
            self.history.append(el)

    def _get(self):
        return super()._get()

    def __contains__(self, element):
        return element in self.history


def process_videos(queue):
    while True:
        item = queue.get()
        # cmd =('avconv -i {} -t 00:00:10 -threads auto -strict experimental {}'
        cmd = ['avconv', '-y', '-i', shlex.quote(item['file']),
               '-strict', 'experimental', '-preset', 'veryfast',
               '-vf', 'scale=-2:320,format=yuv420p',
               # '-t', '00:01:00',
               shlex.quote(item['tmpname'])]

        FNULL = open(os.devnull, 'w')
        subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
        queue.task_done()


def measured_convert(cmd):
    print('measuring:', cmd)
    start = timer()
    FNULL = open(os.devnull, 'wb')
    subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    # subprocess.call(cmd)
    result = timer()-start
    print('it took time:', result)
    return result


def benchmark(input_file):
    output_template = '/home/borsuk/workspace/lfs-test/video_{}.mp4'

    base_cmd = ['avconv', '-y', '-i', input_file, '-t', '00:01:00',
                '-strict', 'experimental']

    presets = {
        'standard': base_cmd[:],
        'fast': base_cmd[:] + ['-preset', 'veryfast'],
        'lossy_fast': base_cmd[:] + ['-preset', 'veryfast', '-crf', '32'],
        'resample': base_cmd[:] + ['-vf', 'scale=-2:320,format=yuv420p'],
        'fast_resample': base_cmd[:] + ['-preset', 'veryfast',
                                        '-vf', 'scale=-2:320,format=yuv420p'],
        'lossy_fast_resample': base_cmd[:] + ['-preset', 'veryfast', '-crf', '32',
                                           '-vf', 'scale=-2:320,format=yuv420p'],
    }

    results = {preset: measured_convert(cmd + [output_template.format(preset)])
               for (preset, cmd) in presets.items()}

    print(results)
    return results


def main():
    # input_directory = ('/home/borsuk/video/pluralsight/game programming with'
    #                    ' python and pygame/02. hello world in pygame/')
    input_directory = ('/home/borsuk/video/blade.and.soul.720/')

    results = {file_name: benchmark(os.path.join(input_directory, file_name))
               for file_name in os.listdir(input_directory)}

    print('\n\n\nFinal resulst:')
    for f, r in results.items():
        print(f)
        print(r)

    # input_file = ('/home/borsuk/video/pluralsight/Game Programming with Python'
    #               ' and PyGame/02. Hello World in PyGame/05. Using the mouse'
    #               ' inside the application.wmv')
    # results = benchmark(input_file)

if __name__ == "__main__":
    main()
