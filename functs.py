import socket
import sys
import os


def recvFile(socket,filename):
    #need to deny overwriting files
    status=True
    try:
        file=open(filename,'xb')
        data=socket.recv(2**25)
        data=data.decode()
        file.write(data)
    except:
        status=False
    #copy data sent  from client
    #if succesful or failed return  the status
    return status

def sendFile(socket,filename):
    status=True
    try:
        file=open(filename,'b')
        fileData=file.read()
        socket.sendall(fileData.encode())
    except:
        status=False
    return status

def sendListing(socket):
    status=True
    try:
        listing=str(os.listdir())
        socket.sendall(listing.encode())
    except:
        status=False
    return status
    
def recvListing(socket):
    status=True
    try:
        listing=socket.recv(2**25)
        listing=listing.decode()
        print(listing)
    except:
        status=False
    return status
