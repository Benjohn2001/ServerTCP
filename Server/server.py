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

#Exception to handle the CTRL-C exit
try:
    #Starting the socket
    serverSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(("", int(sys.argv[1])))    
    ipAddress=socket.gethostbyname('localhost')
    print("Ip: "+ipAddress+" Port: "+sys.argv[1]+" server up and running")
    serverSock.listen(5)
    #Connecting to the client and receiving the request
    while True:
        clientSock,clientAddress=serverSock.accept()
        request=clientSock.recv(1024)
        request=request.decode()
        request=request.split(" ")
        #Deciding what function to call based on the request
        if request[0]=="put":
            filename=request[1]
            status,error=recvFile(clientSock,filename)
        if request[0]=="get":
            filename=request[1]
            status,error=sendFile(clientSock,filename)
        if request[0]=="list":
            status,error=sendListing(clientSock)
        #Printing the status of the request
        if status==False:
            if len(request)>1:
                print("Failed - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+request[0]+" "+request[1]+" "+error)
            else:
                print("Failed - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+request[0]+" "+error)
        if status==True:
            if len(request)>1:
                print("Success - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+request[0]+" "+request[1])
            else:
                print("Success - IP: "+ipAddress+" Port: "+sys.argv[1]+" Request: "+request[0])
        clientSock.close()

except KeyboardInterrupt:
    print(" Quitting")

        
    

