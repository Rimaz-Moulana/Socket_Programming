import socket
import sys
import threading

clients = []
topics = {}

def handle_client(client_socket, address):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            # Split the received message into topic and content
            topic, message = data.split(':', 1)

            if topic in topics:
                subscribers = topics[topic]
                for subscriber in subscribers:
                    if subscriber != client_socket:
                        subscriber.sendall(message.encode())

    finally:
        client_socket.close()
        remove_client(client_socket)
        print(f"Client disconnected: {address[0]}:{address[1]}")

def add_client(client_socket, topic):
    clients.append(client_socket)
    if topic in topics:
        topics[topic].append(client_socket)
    else:
        topics[topic] = [client_socket]

def remove_client(client_socket):
    clients.remove(client_socket)
    for topic in topics.values():
        if client_socket in topic:
            topic.remove(client_socket)

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

            # Receive the client's topic as a separate message
            topic = client_socket.recv(1024).decode()
            add_client(client_socket, topic)

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
