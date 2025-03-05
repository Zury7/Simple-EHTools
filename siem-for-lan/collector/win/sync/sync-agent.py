import socket
import time
import win32evtlog

def get_windows_logs(log_type="Application"):
    logs = []
    hand = win32evtlog.OpenEventLog(None, log_type)

    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)

    for event in events[:10]:  # Get last 10 logs for testing
        logs.append(f"Time: {event.TimeGenerated} | Event ID: {event.EventID} | Source: {event.SourceName}")

    return "\n".join(logs)

def start_agent(server_ip="127.0.0.1", server_port=5000):
    while True:
        try:
            print(f"Connecting to server at {server_ip}:{server_port}...")

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            logs = get_windows_logs()
            client_socket.send(logs.encode())

            client_socket.close()
            print("Logs sent successfully!")

        except Exception as e:
            print(f"Error: {e}")

        print("Waiting 10 minutes before sending logs again...")
        time.sleep(600)  # Wait 10 minutes before sending again

if __name__ == "__main__":
    start_agent()
