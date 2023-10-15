from fileinput import filename
import socket, sys

# take in arguments
listenPort = int(sys.argv[1])
keyName = sys.argv[2]

#temp debug to check args
print(listenPort)
print(keyName)

keys = []

with open(keyName, 'r', encoding='ascii') as file:
    for i, line in enumerate(file):
        keys.append(line.strip())

#establish socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), listenPort))
#temp print to get host name
print(socket.gethostname())
s.listen(5)

while True:
    #listen for connection
    clientSocket, address = s.accept()
    
    #temporary close, tests one connection
    s.close()
    break
