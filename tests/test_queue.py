from app.background_processor import UniqueQueue
import threading

class TestUnique():
    def setup_method(self, method):
        self.q = UniqueQueue(5)


    def test_add(self):
        elem = {'a': 'al', 'b': 'bl'}
        elem2 = {'f': 'fl', 'g': 'gl'}
        self.q.put(elem)

        assert elem in self.q.queue
        assert elem in self.q
        assert elem2 not in self.q.queue
        assert elem2 not in self.q

    def test_get(self):
        elem = {'a': 'al', 'b': 'bl'}
        elem2 = {'f': 'fl', 'g': 'gl'}
        self.q.put(elem)
        self.q.put(elem2)

        assert self.q.queue == [elem, elem2]

        e = self.q.get()
        assert e == elem
        assert self.q.queue == [elem2]

