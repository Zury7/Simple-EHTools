import socket
import threading

# File to save results
OUTPUT_FILE = "port_scan_results.txt"

def scan_port(ip, port, open_ports):
    """Scan a specific port on a given IP and identify the service."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set timeout for connection attempt
            if s.connect_ex((ip, port)) == 0:
                try:
                    service = socket.getservbyport(port)  # Get service name
                except:
                    service = "Unknown Service"
                
                open_ports.append((port, service))
                print(f"[+] Port {port} is OPEN ({service})")
    except Exception:
        pass  # Ignore errors

def port_scanner(ip, start_port=1, end_port=1024):
    """Scans ports within the given range and saves results to a file."""
    open_ports = []
    threads = []

    print(f"🔍 Scanning {ip} from port {start_port} to {end_port}...")

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    with open(OUTPUT_FILE, "w") as file:
        file.write(f"Open ports on {ip}:\n")
        for port, service in open_ports:
            file.write(f"Port {port} is OPEN ({service})\n")

    print(f"✅ Scan complete! Results saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter start port (default: 1): ") or 1)
    end_port = int(input("Enter end port (default: 1024): ") or 1024)

    port_scanner(target_ip, start_port, end_port)
