from client import Subscriber
import time
import signal
from functools import partial

def cbk(data):
    print(time.time())


if __name__ == '__main__':
    sub = Subscriber('localhost:9002', route='/test', callback=cbk)
    sub.start()

    signal.signal(signal.SIGINT, lambda a,b: sub.stop())
    while not sub.isStop:
        pass

    