import os
import sys
import socket
import _thread

def parse_http_req(request):
    lines = request.split('\n')
    cmd, path, prot = lines[0].split()
    return cmd, path.strip('/')

def gobble_file(filename, flag):
    fin = open(filename, flag)
    content = fin.read()
    fin.close()
    return content    

def do_request(connectionSocket):

    request = connectionSocket.recv(1024).decode()

    basepath = os.getcwd()
    cmd, path = parse_http_req(request)

    # .get_native_id() doesn't work in Python3.7 and crashes within
    #  the container
    #print('##', cmd, path, _thread.get_native_id())

    default = 'HTTP/1.1 200 OK\r\n\r\nDefault response'

    if len(path) > 0:
        #filename = os.path.join(basepath, path)
        filename = path
        if os.path.exists(filename):
            if filename.endswith('.html'):
                content = gobble_file(filename, 'r')
                connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                connectionSocket.send(content.encode())                
            elif filename.endswith('.jpg'):
                content = gobble_file(filename, 'rb')
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: image/jpeg\r\n".encode())
                connectionSocket.send("Accept-Ranges: bytes\r\n\r\n".encode())
                connectionSocket.send(content)
        else:
            resp = 'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>'
            resp += '<p>' + filename
            connectionSocket.send(resp.encode())
    else:
        connectionSocket.send(default.encode())
    
    # Close the connection
    connectionSocket.close()
    
        
def main(serverPort):
    
    # Create the server socket object
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the server socket to the port
    serverSocket.bind(('',serverPort))
    
    # Start listening for new connections
    serverSocket.listen(1)
    print('The server is ready to receive messages on port:', serverPort)

    while True:
        # Accept a connection from a client
        connectionSocket, addr = serverSocket.accept()

        # Retrieve the message sent by the client
        #do_request(connectionSocket)

        # Handle each connection in a separate thread
        _thread.start_new_thread(do_request, (connectionSocket,))
        
if __name__ == '__main__':

    # Listening port for the server
    if len(sys.argv) <= 1:
        serverPort = 8080
    else:
        serverPort = int(sys.argv[1])

    main(serverPort)
    
