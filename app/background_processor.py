import queue
import subprocess


class UniqueQueue(queue.Queue):
    """Docstring for UniqueQueue. """

    def _init(self, maxsize):
        self.queue = []

    def _put(self, el):
        if el not in self.list:
            self.queue.append(el)

    def _get(self):
        return self.queue.pop()


def process_videos(queue):
    while True:
        item = queue.get()
        print(item)
        cmd = ('avconv -i {} -t 00:00:10 -strict experimental {}'
               .format(item['f1'], item['f2']))
        subprocess.call(cmd, shell=True)
        queue.task_done()
