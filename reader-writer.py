import threading
import time

readCount=0
write = threading.Semaphore()
mutex = threading.Semaphore()
