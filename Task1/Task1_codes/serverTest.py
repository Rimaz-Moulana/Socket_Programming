import socket


def server_program():
    #get the check hostname
    host = socket.gethostname()
    port = 5000
    
    server_socket = socket.socket() # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host,port))
    
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn,addr=server_socket.accept()
    print("connection from: "+ str(addr))
    while True:
        #receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data or (str(data) == "terminate"):
            print("client disconnected from the server")
            break
        print("from connected user: "+ str(data))
        data = input('->')
        conn.send(data.encode())#send data to the client
        
    conn.close() #close connection
    
if __name__ == '__main__':
    server_program()
