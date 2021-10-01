import socket
import sys
import os

#Function to receive the file specified with the filename parameter
def recvFile(socket,filename):
    status=True
    error=("")
    print(filename)
    try:
        try:
            with open(filename,'xb') as file:
                while True:
                    data=socket.recv(4096)
                    if not data:
                        break
                    file.write(data)
        except:
            print("File already exists ")
            status=False
            error=("File already exists ")
    except:
        status=False
    return status,error

#Function to send the given file through the socket
def sendFile(socket,filename):
    status=True
    error=("")
    totalSent=0
    try:
        try:
            with open(filename,'rb') as file:
                while True:
                    fileData=file.read(4096)
                    if not fileData:
                        break
                    socket.sendall(fileData)
                    totalSent+=len(fileData)
        except FileNotFoundError:
            print("File does not exist ")
            status=False
            error=("File does not exist ")
    except:
        status=False
        print("File already exists ")
        error=("File already exists ")
    return status,error

#Function to send the listing through the socket
def sendListing(socket):
    status=True
    error=("")
    try:
        listing=str(os.listdir())
        socket.sendall(listing.encode())
    except:
        status=False
        print("Listing cannot be found ")
        error=("Listing cannot be found ")
    return status, error

#Function to receive the listing
def recvListing(socket):
    status=True
    error=("")
    try:
        listing=socket.recv(2**25)
        listing=listing.decode()
        listing=listing.split()
        for i in range(0,len(listing)):
            print(listing[i])
    except:
        status=False
        print("Listing not received ")
        error=("Listing not received ")
    return status, error

#Exception handling for connection loss
try:
    #Connection to the socket
    clientSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((sys.argv[1], int(sys.argv[2])))
    ipAddress=socket.gethostbyname(sys.argv[1])
    if len(sys.argv)==4:
        command=sys.argv[3]
    else:
        command=sys.argv[3]+" "+sys.argv[4]
    #sending the request to the server
    clientSocket.sendall(command.encode())
    #calling the specific function for the request passed in
    if sys.argv[3]=="put":
        filename=sys.argv[4]
        status,error=sendFile(clientSocket,filename)
    if sys.argv[3]=="get":
        filename=sys.argv[4]
        status,error=recvFile(clientSocket,filename)
    if sys.argv[3]=="list":
        status,error=recvListing(clientSocket)
    #reporting on the status of the request
    if status==False:
        if len(sys.argv)==4:
            print("Failed - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+sys.argv[3]+" "+error)
        else:
            print("Failed - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+sys.argv[3]+" "+sys.argv[4]+" "+error)
    if status==True:
        if len(sys.argv)==4:
            print("Success - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+sys.argv[3])
        else:
            print("Success - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+sys.argv[3]+" "+sys.argv[4])

    clientSocket.close()

except:
    print("server.py  must not be running")



