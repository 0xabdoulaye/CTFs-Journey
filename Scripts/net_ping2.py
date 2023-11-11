import subprocess
import threading
import platform
import ipaddress
import queue

def is_reachable(ip, results_queue):
    try:
        # Determine the appropriate ping command based on the platform
        ping_cmd = ['ping', '-n', '1', ip] if platform.system().lower() == "windows" else ['ping', '-c', '1', ip]
        subprocess.check_output(ping_cmd, timeout=2)
        results_queue.put(ip)
    except Exception:
        pass

def main():
    # Replace the "10.10.12.0" with your appropriate subnet.
    subnet = ipaddress.IPv4Network("10.10.10.0/24")

    results_queue = queue.Queue()
    threads = []
    for ip in subnet.hosts():
        thread = threading.Thread(target=is_reachable, args=(str(ip), results_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish their execution
    for thread in threads:
        thread.join()

    # Print reachable IP addresses
    while not results_queue.empty():
        ip = results_queue.get()
        print(f"{ip} is reachable.")

if __name__ == "__main__":
    main()
