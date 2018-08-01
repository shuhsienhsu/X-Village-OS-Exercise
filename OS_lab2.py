import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir, queue_buffer):
    test = os.listdir(top_dir)
    #count = 0
    for i in test:
        if(os.path.isdir(os.path.join(top_dir, i))):
            #print(os.path.join(top_dir, i))
            queue_buffer.put(os.path.join(top_dir, i))
            producer(os.path.join(top_dir, i), queue_buffer)
            #count += 1
    # Search sub-dir in top_dir and put them in queue

def consumer(queue_buffer):
    global file_count
    try:
        dir = queue_buffer.get(True, 1)
        
        files = os.listdir(dir)
        for i in files:
            if(os.path.isfile(os.path.join(dir, i))):
                print(os.path.join(dir, i))
                lock.acquire()
                file_count += 1
                lock.release()
                #print(file_count)
        
    except Exception:
        return
    # search file in directory

def main():
    queue.put('./testdata')
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()