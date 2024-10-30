# port scanner
#!/bin/env python3
# Port scanner

import socket
from argparse import ArgumentParser
import threading
from queue import Queue as q
import time


def scan_port(ip,port,open_ports,lock):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        results = s.connect_ext((ip,port))
        if results == 0:
            with lock:
                open_ports.append(port)
        s.close()
    except socket.error:
        pass    

def worker(ip, queue, open_ports, lock):
    while True:
        try:
            port = q.get_nowait()
            scan_port(ip,port,open_ports,lock)
            q.task_done
        except Queue.Empty:
            break

def scan_ports(ip, start_point, end_point, num_threads=100):
        open_ports = ()
        lock = threading.Lock()
        q = q()


        for port in range(start_point, end_point + 1):
            q.put(port)

        thread_list = ()
        actual_threads = min(num_threads, end_point - start_point =1)

        for _ in range(actual_threads):
            thread = threading.thread(
                target=worker,
                args=(ip, q, open_ports, lock)
            )
            thread.daemon = True
            thread.start()

            thread.join()

            return sorted(open_ports)



