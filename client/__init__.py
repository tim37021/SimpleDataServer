from websocket import create_connection
from queue import Queue
import time
from threading import Thread


class Timer(object):
    """
    See: https://hg.python.org/cpython/file/2.7/Lib/threading.py#l1079
    """
    def __init__(self, interval, func):
        self._t = Thread(target=self._run)
        self._stop = False
        self._func = func
        self._interval = interval

    def start(self):
        self._t.start()

    def stop(self):
        self._stop = True

    @property
    def isStop(self):
        return self._stop

    def _run(self):
        import time
        while not self._stop:
            t = time.time()
            self._func()
            time.sleep(self._interval-(time.time()-t))


class Publisher(object):
    def __init__(self, server, route, freq):
        self._ws = create_connection('ws://%s%s/publish'%(server, route))
        self._freq = freq
        self._timer = None
        self._queue = Queue()
    
    """
        publish
        data: data to be publish in the next frame
    """
    def publish(self, data):
        self._queue.put(data)

    def start(self):
        self._timer = Timer(1/self._freq, self._sendPacket)
        self._timer.start()

    def stop(self):
        self._timer.stop()

    @property
    def isStop(self):
        return self._timer.isStop


    def _sendPacket(self):
        data = None
        while not self._queue.empty():
            data = self._queue.get_nowait()

        if data == None:
            data = self._queue.get(timeout=0.001)

        if type(data) is str:
            self._ws.send(data)
        else:
            self._ws.send_binary(data)

class Subscriber(object):
    def __init__(self, server, route, callback):
        self._ws = create_connection('ws://%s%s/subscribe'%(server, route))
        self._callback = callback
        self._stop = False
        
    def start(self):
        self._t = Thread(target=self._run)
        self._t.start()

    def stop(self):
        self._stop = True

    def _run(self):
        while not self._stop:
            self._callback(self._ws.recv())

    @property
    def isStop(self):
        return self._stop

class Chat(object):
    def __init__(self, server, route, callback):
        self._ws = create_connection('ws://%s%s/chat'%(server, route))
        self._callback = callback
        self._stop = False

    def send(self, data):
        if type(data) is str:
            self._ws.send(data)
        else:
            self._ws.send_binary(data)
        
    def start(self):
        self._t = Thread(target=self._run)
        self._t.start()

    def stop(self):
        self._stop = True

    def _run(self):
        while not self._stop:
            self._callback(self._ws.recv())

    @property
    def isStop(self):
        return self._stop