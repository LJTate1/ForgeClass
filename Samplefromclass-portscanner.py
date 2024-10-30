#!/usr/bin/env python3
"""
Basic Port Scanner - Procedural Version
A simple multi-threaded port scanner using basic Python concepts.

"""

import socket         # For network connections
import argparse       # For command-line argument parsing
import threading      # For creating and managing threads
from queue import Queue   # For thread-safe queueing of tasks
import time           # For timing the duration of the scan

def scan_port(ip, port, open_ports, lock):
    """
    Attempt to connect to a specific port on a given IP address to determine if it's open.

    Args:
        ip (str): Target IP address.
        port (int): Port number to scan.
        open_ports (list): Shared list to store open ports.
        lock (threading.Lock): A lock to ensure thread-safe access to shared resources.
    """
    try:
        # Create a new socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout to prevent hanging on unresponsive ports
        sock.settimeout(1)
        
        # Attempt to connect to the target IP and port
        result = sock.connect_ex((ip, port))
        
        # If the result is 0, the port is open
        if result == 0:
            # Acquire the lock before modifying the shared list
            with lock:
                open_ports.append(port)
                
        # Close the socket after the attempt
        sock.close()
        
    except socket.error:
        # Ignore any socket errors and move on
        pass

def worker(ip, queue, open_ports, lock):
    """
    Worker function run by each thread to process ports from the queue.

    Args:
        ip (str): Target IP address.
        queue (Queue): Queue containing ports to scan.
        open_ports (list): Shared list to store open ports.
        lock (threading.Lock): Lock for thread-safe access to shared resources.
    """
    while True:
        try:
            # Get a port number from the queue without blocking
            port = queue.get_nowait()
            # Scan the port
            scan_port(ip, port, open_ports, lock)
            # Signal that the task is done
            queue.task_done()
        except Queue.Empty:
            # If the queue is empty, exit the loop
            break

def scan_ports(ip, start_port, end_port, num_threads=100):
    """
    Scan a range of ports on a given IP address using multiple threads.

    Args:
        ip (str): Target IP address.
        start_port (int): First port to scan.
        end_port (int): Last port to scan.
        num_threads (int): Number of threads to use for scanning.

    Returns:
        list: A sorted list of open ports.
    """
    open_ports = []            # Shared list to store open ports
    lock = threading.Lock()    # Lock to synchronize access to open_ports
    queue = Queue()            # Queue to hold the ports to be scanned

    # Add all ports in the specified range to the queue
    for port in range(start_port, end_port + 1):
        queue.put(port)

    thread_list = []  # List to keep track of thread references
    
    # Determine the actual number of threads to use
    actual_threads = min(num_threads, end_port - start_port + 1)

    # Start the worker threads
    for _ in range(actual_threads):
        # Create a new Thread object targeting the worker function
        thread = threading.Thread(
            target=worker,
            args=(ip, queue, open_ports, lock)
        )
        thread.daemon = True  # Set as daemon so it exits when main thread does
        thread.start()        # Start the thread
        thread_list.append(thread)

    # Wait until all tasks in the queue have been processed
    queue.join()
    
    # Wait for all threads to complete execution
    for thread in thread_list:
        thread.join()

    # Return the sorted list of open ports
    return sorted(open_ports)

def print_results(ip, open_ports, duration):
    """
    Print the results of the port scan to the console.

    Args:
        ip (str): The IP address that was scanned.
        open_ports (list): List of open ports found during the scan.
        duration (float): Total time taken to complete the scan.
    """
    print("\nScan completed!")
    print(f"Duration: {duration:.2f} seconds")
    print("\nResults:")
    
    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            try:
                # Attempt to get the service name for the port
                service = socket.getservbyport(port)
            except OSError:
                # If the service name is not found, mark it as unknown
                service = "unknown"
            print(f"  Port {port}: {service}")
    else:
        print("\nNo open ports found")

def main():
    """Main function to parse arguments and initiate the port scan."""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Basic Port Scanner')
    parser.add_argument('target', help='Target IP address or hostname')
    parser.add_argument(
        '-s', '--start',
        type=int,
        default=1,
        help='Starting port (default: 1)'
    )
    parser.add_argument(
        '-e', '--end',
        type=int,
        default=1024,
        help='Ending port (default: 1024)'
    )
    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=100,
        help='Number of threads to use (default: 100)'
    )

    args = parser.parse_args()

    try:
        # Resolve the hostname to an IP address
        target_ip = socket.gethostbyname(args.target)
        
        print(f"\nStarting scan on {args.target} ({target_ip})")
        print(f"Port range: {args.start}-{args.end}")
        print(f"Using {args.threads} threads")
        print("\nScanning...")

        # Start timing the scan
        start_time = time.time()

        # Run the port scan
        open_ports = scan_ports(
            target_ip,
            args.start,
            args.end,
            args.threads
        )

        # Calculate the total duration of the scan
        duration = time.time() - start_time

        # Print the scan results
        print_results(target_ip, open_ports, duration)

    except socket.gaierror:
        # Handle errors in resolving the hostname
        print("Error: Could not resolve hostname")
    except KeyboardInterrupt:
        # Gracefully handle user interruption
        print("\nScan interrupted by user")
    except Exception as e:
        # Catch any other exceptions and print the error message
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

