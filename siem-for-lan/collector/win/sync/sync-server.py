import socket

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        # Receive logs from agent
        logs = client_socket.recv(8192).decode()

        if logs:
            print("Logs received, saving to file...")
            with open("received_logs.txt", "a", encoding="utf-8") as file:
                file.write(logs + "\n" + "-"*50 + "\n")
            print("Logs saved successfully!")

        client_socket.close()

if __name__ == "__main__":
    start_server()
