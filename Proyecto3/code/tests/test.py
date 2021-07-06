import sys
import threading
import time
import queue

def add_input(input_queue):
    while True:
        # input_queue.put(sys.stdin.read(1))
        input_queue.put(input(""))

def foobar():
    input_queue = queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    last_update = time.time()
    while True:

        if time.time()-last_update>0.5:
            # sys.stdout.write(".")
            # sys.stdout.flush()
            print(".", end='', flush=True)
            last_update = time.time()

        if not input_queue.empty():
            string = input_queue.get()
            print("\ninput:", string)
            if string == 'q':
                input_thread.join()
                return

foobar()