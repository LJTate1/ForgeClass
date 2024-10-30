# NewPortScaner
#!/usr/bin/env python3
"""
Basic Port Scanner - Procedural Version
A simple multi-threaded port scanner using basic Python concepts.
"""

import socket
import argparse
import threading
from queue import Queue, Empty
import time
import sys

def print_progress(current, total, bar_length=50):
    """
    Print a progress bar showing scan progress.
    
    Args:
        current (int): Current progress value
        total (int): Total value for 100% progress
        bar_length (int): Length of the progress bar in characters
    """
    progress = float(current) / total
    filled_length = int(progress * bar_length)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    percent = int(progress * 100)
    sys.stdout.write(f'\rScanning: [{bar}] {percent}% ({current}/{total})')
    sys.stdout.flush()
    if current == total:
        print()  # New line when complete

def scan_port(ip, port, open_ports, lock):
    """
    Attempt to connect to a specific port on a given IP address.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            with lock:
                open_ports.append((port, get_service_name(port)))
        sock.close()
    except socket.error:
        pass

def get_service_name(port):
    """Get service name for a port number."""
    try:
        return socket.getservbyport(port)
    except (OSError, socket.error):
        return "unknown"

def worker(ip, queue, open_ports, lock, progress_counter, total_ports):
    """Worker function for threading."""
    while True:
        try:
            port = queue.get_nowait()
            scan_port(ip, port, open_ports, lock)
            with lock:
                progress_counter[0] += 1
                print_progress(progress_counter[0], total_ports)
            queue.task_done()
        except Empty:
            break

def scan_ports(ip, start_port, end_port, num_threads=100):
    """Scan a range of ports on a given IP address."""
    open_ports = []
    lock = threading.Lock()
    queue = Queue()
    progress_counter = [0]  # Use list to allow modification in threads
    total_ports = end_port - start_port + 1

    for port in range(start_port, end_port + 1):
        queue.put(port)

    thread_list = []
    actual_threads = min(num_threads, total_ports)

    for _ in range(actual_threads):
        thread = threading.Thread(
            target=worker,
            args=(ip, queue, open_ports, lock, progress_counter, total_ports)
        )
        thread.daemon = True
        thread.start()
        thread_list.append(thread)

    queue.join()
    for thread in thread_list:
        thread.join()

    return sorted(open_ports)

def print_results(target, ip, open_ports, duration):
    """Print scan results in a formatted table."""
    print("\n" + "="*70)
    print(f"Scan Results for {target}")
    print(f"Scan duration: {duration:.2f} seconds")
    print("="*70 + "\n")

    if open_ports:
        print(f"Found {len(open_ports)} open ports:\n")
        print("PORT".ljust(10) + "SERVICE".ljust(20))
        print("-" * 30)
        for port, service in open_ports:
            print(f"{str(port).ljust(10)}{service.ljust(20)}")
    else:
        print("No open ports found")
    print()

def main():
    """Main function to parse arguments and initiate the port scan."""
    parser = argparse.ArgumentParser(description='Less Basic Port Scanner')
    parser.add_argument('target', help='Target IP address or hostname')
    parser.add_argument('-s', '--start', type=int, default=1,
                      help='Starting port (default: 1)')
    parser.add_argument('-e', '--end', type=int, default=1024,
                      help='Ending port (default: 1024)')
    parser.add_argument('-t', '--threads', type=int, default=100,
                      help='Number of threads (default: 100)')
    parser.add_argument('-o', '--output', help='Output file name')

    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.target)
        
        print("\nStarting Less Basic Port Scanner")
        print(f"Target: {args.target} ({ip})")
        print(f"Port range:{args.start}-{args.end}")
        print(f"Threads: {args.threads}")
        print(f"Timeout 1.0 seconds\n")

        start_time = time.time()
        open_ports = scan_ports(ip, args.start, args.end, args.threads)
        duration = time.time() - start_time

        print_results(args.target, ip, open_ports, duration)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Scan Results for {args.target} ({ip})\n")
                f.write(f"Duration: {duration:.2f} seconds\n\n")
                if open_ports:
                    f.write("Open ports:\n")
                    for port, service in open_ports:
                        f.write(f"Port {port}: {service}\n")
                else:
                    f.write("No open ports found\n")

    except socket.gaierror:
        print("Error: Could not resolve hostname")
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

