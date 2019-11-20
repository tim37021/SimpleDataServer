from client import Publisher
import time

if __name__ == '__main__':
    pub = Publisher('localhost:9002', route='/test', freq=10)
    pub.start()
    while True:
        pub.publish('123')
        time.sleep(0.1)