import socket
import sys
import threading

publishers = []
subscribers = []

def handle_client(client_socket, address):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Check if the client is a publisher or subscriber
            if client_socket in publishers:
                # Broadcast the message to all subscribers
                for subscriber in subscribers:
                    subscriber.sendall(data.encode())
            elif client_socket in subscribers:
                # Publishers should not receive messages from other publishers
                pass

    finally:
        client_socket.close()

        # Remove the client from the appropriate list
        if client_socket in publishers:
            publishers.remove(client_socket)
        elif client_socket in subscribers:
            subscribers.remove(client_socket)

        print(f"Client disconnected: {address[0]}:{address[1]}")

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', port)
    print(f"Starting server on {server_address[0]}:{server_address[1]}")

    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Waiting for clients to connect...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address[0]}:{client_address[1]}")

            # Determine whether the client is a publisher or subscriber
            mode = client_socket.recv(1024).decode()
            if mode == "PUBLISHER":
                publishers.append(client_socket)
            elif mode == "SUBSCRIBER":
                subscribers.append(client_socket)
            else:
                print(f"Unknown mode for client: {client_address[0]}:{client_address[1]}")

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    finally:
        server_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
