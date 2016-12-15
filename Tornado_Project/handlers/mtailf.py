import time
import asyncio

def follow(thefile, target):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


@asyncio.coroutine
def grep(pattern, target):
    while True:
        line = yield
        if pattern in line:
            target.send(line)


@asyncio.coroutine
def printer():
    while True:
        line = yield
        print(line)

if __name__ == "__main__":
    f = open()
    follow(f, grep("python",printer()))   