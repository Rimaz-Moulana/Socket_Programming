import socket


def client_program():
    host = socket.gethostname()
    port = 5000
    
    client_socket = socket.socket()
    client_socket.connect((host,port)) #connect to server
    
    message = input("->") #take input
    
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode() #recieve response
        
        print('Recieve from server:' + data) #show in terminal
        
        message = input("->") #again take input
        
    client_socket.close()
    
if __name__ == '__main__':
    client_program()