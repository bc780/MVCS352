from fileinput import filename
import socket, sys


# take in arguments
listenPort = sys.argv[1]
keyName = sys.argv[2]

#temp debug to check args
print(listenPort)
print(keyName)

#establish socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), listenPort))
s.listen(5)

while True:
    #listen for connection
    clientSocket, address = s.listen()
    
    #temporary close, tests one connection
    s.close()
    break