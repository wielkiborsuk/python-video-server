import os
import queue
import shlex
import subprocess


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
        print(item)
        # cmd = ('avconv -i {} -t 00:00:10 -threads auto -strict experimental {}'
        cmd = ('avconv -i {} -threads auto -strict experimental {}'
               .format(shlex.quote(item['file']), shlex.quote(item['tmpname'])))
        FNULL = open(os.devnull, 'w')
        subprocess.call(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        item['res'] = True
        queue.task_done()
