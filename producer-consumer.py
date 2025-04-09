import threading
import time

capacity = 10
enter = 0
exit = 0
buffer = [-1 for i in range(capacity)]
producerArray = []
consumerArray = []

mutex = threading.Semaphore()
empty = threading.Semaphore(capacity)
full = threading.Semaphore(0)


class Producer(threading.Thread):
    def run(self):
        global capacity, enter, exit, buffer, mutex, empty, full, producerArray
        print(buffer, "Buffer at starting of producer..............")
        items = 0
        counter = 0
        while items < 20:
            empty.acquire()
            mutex.acquire()
            counter += 1
            buffer[enter] = counter
            enter = (enter + 1) % capacity
            print("Producer produced : ", counter)
            producerArray.append(counter)
            mutex.release()
            full.release()
            time.sleep(1.5)
            items += 1
            print(buffer, "Buffer..............")


class Consumer(threading.Thread):
    def run(self):
        global capacity, enter, exit, buffer, mutex, empty, full, consumerArray
        print(buffer, "Buffer at starting of consumer..............")
        items = 0
        while items < 20:
            full.acquire()
            mutex.acquire()
            item = buffer[exit]
            exit = (exit + 1) % capacity
            print("Consumer consumed item : ", item)
            consumerArray.append(item)
            mutex.release()
            empty.release()
            time.sleep(3)
            items += 1
            print(buffer, "Buffer..............")


producer = Producer()
consumer = Consumer()

producer.start()
consumer.start()

producer.join()
consumer.join()

print(producerArray)
print(consumerArray)
