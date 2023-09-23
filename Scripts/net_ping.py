import subprocess
import threading
import platform

def ping_ip(ip):
    try:
        # Determine the appropriate ping command based on the platform
        ping_cmd = ['ping', '-n', '1', ip] if platform.system().lower() == "windows" else ['ping', '-c', '1', ip]
        subprocess.check_output(ping_cmd, timeout=2)
        print(f"{ip} is reachable.")
    except subprocess.TimeoutExpired:
        print(f"{ip} is not reachable.")
    except subprocess.CalledProcessError:
        print(f"{ip} is not reachable.")

def main():
    # Replace the "0" in the IP address with your appropriate subnet.
    threads = []
    for i in range(1, 256):
        ip = f"10.150.150.{i}"
        thread = threading.Thread(target=ping_ip, args=(ip,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish their execution
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
