import socket
import sys
import threading

def handle_server_messages(server_socket):
    try:
        while True:
            data = server_socket.recv(1024).decode()
            if not data:
                break
            print(f"Received from server: {data}")

    finally:
        server_socket.close()
        print("Disconnected from server.")
        sys.exit()

def start_client(server_ip, port, mode, topic):
    server_address = (server_ip, port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(server_address)
        print(f"Connected to server: {server_address[0]}:{server_address[1]}")

        # Send the client's topic as a separate message
        client_socket.sendall(topic.encode())

        # Start a new thread to handle incoming server messages
        server_thread = threading.Thread(target=handle_server_messages, args=(client_socket,))
        server_thread.start()

        if mode == "PUBLISHER":
            while True:
                message = input("Enter a message (or 'terminate' to quit): ")
                full_message = f"{topic}:{message}"
                client_socket.sendall(full_message.encode())
                if message == "terminate":
                    break
        elif mode == "SUBSCRIBER":
            print("Subscribing to the server...")
            while True:
                pass  # Keep the client running to receive server messages

    finally:
        client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python client.py <server_ip> <port> <mode> <topic>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    mode = sys.argv[3]
    topic = sys.argv[4]
    start_client(server_ip, port, mode, topic)
