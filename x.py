import os
import threading

host = '34.16.169.60'

def ping():
    for _ in range(100):
        response = os.system(f'ping -c 1 {host}')
        if response == 0:
            print('pong')
        else:
            print('ruh roh')

if __name__ == '__main__':
    threads = []

    for i in range(50):
        t = threading.Thread(target=ping)
        t.daemon = True
        threads.append(t)

    for i in range(50):
        threads[i].start()

    for i in range(50):
        threads[i].join()
