# Name: Sushmitha Nagarajan, Student ID: 1001556348

# Multithread_Server.py
from socket import *  # Import socket module
import threading      # Import Threading module

#port = 9090           # Reserve the port for your service


# Code referred from http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php and
# http://crystal.uta.edu/~datta/teaching/cse5344_3/Programming%20Assignment%201_reference_Python.pdf
port = int(input("Enter Port Number: "))
print (port)

class MyThread(threading.Thread):               # Create a class 'MyThread'
    def __init__(self, ip, port, sock):         # Initialize the thread with the given parameters
        threading.Thread.__init__(self)
        self.ip = ip                            # Assign IP to self.ip
        self.port = port                        # Assign Port to self.port
        self.sock = sock                        # Assign socket to self.sock
        print(" New thread created for " + ip + ":" + str(port))   # Print the IP and port number of the client

    def run(self):                              # Initiate the process to read the message
        try:                                    # Initiate the try block if it doesnt have an exception
            message = self.sock.recv(1024)      # Get 1024 bytes of message from the client
            print(message)                      # Print the message received
            if len(message.split()) > 0:        # Split the message
                print(message.split()[1])       # Filename is store in the message.split[1] and print the same
            filename = message.split()[1]       # Store the filename in a variable
            f = open(filename[1:])              # Open the file
            outputdata = f.read()               # Read the file
            f.close()                           # Close the file
            print(outputdata)                   # Print the output data of the file
            # Pass Http/1.1 200 OK and display file in browser
            self.sock.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
            for i in range(0, len(outputdata)): # Output the data on the client requested
                self.sock.send(outputdata[i].encode())      # Send the output data to the client socket
            print('File sent successfully')                 # Print a confirmation message
            self.sock.close()                               # Close the socket
        except IOError:                                     # Set and exception if the file is not found
            self.sock.send(b'&#72;TTP/1.1 404 File not found')  # Send response message for file not found
            #self.sock.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
            self.sock.close()                                # Close Client socket


serverSocket = socket(AF_INET, SOCK_STREAM)                 # Prepare a server socket
threads = [];                                               # Create a variable 'threads' with no input parameters

try:
    serverSocket.bind(("localhost", port))                  # Bind socket
    print('Socket bind complete')                           # Print a confirmation message

except socket.error as msg:                                 # Set an exception if the binding failed
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])    # Display an error message
    sys.exit()                                              # Exit the system if the binding failed

serverSocket.listen(10)                                     # Listen to the client
print('socket is listening....')                            # Print a confirmation message

while True:                                                 # Accept connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()          # Establish the connection
    print('Connected with ' + addr[0] + ':' + str(addr[1]))      # Print IP address and port number of the client
    print(connectionSocket)                                      # Print the connection socket
    # Print the peer name, socket family, socket type, time out value and socket protocol of the client
    print("Peer name: " + str(connectionSocket.getpeername()))
    print('Socket Family: ' + str(connectionSocket.family), 'Socket Type: ' + str(connectionSocket.type),
          'Time out: ' + str(connectionSocket.timeout), 'Socket Protocol: ' + str(connectionSocket.proto))
    New = MyThread(addr[0], addr[1], connectionSocket)          # Initiate multi-threading of the clients
    New.start()                                                 # Start multi-threading
    threads.append(New)                                         # Append new thread
    for t in threads:                                           # Add more clients to the thread
        t.join()