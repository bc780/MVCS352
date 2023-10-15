import socket, sys

#take in arguments
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
msgName = sys.argv[3]
sigName = sys.argv[4]

#temp debug to check args
print(serverName)
print(serverPort)
print(msgName)
print(sigName)

msgSizes = []
msgBytes = []
signatures = []

with open(msgName, 'r', encoding='ascii') as file:
    for i, line in enumerate(fp):
        if i%2==0:
            msgSizes.append(int(line.strip()))
        else:
            bytes = bytes(line.strip(),'ascii')
            msgBytes.append(bytes) 
          
with open(sigName, 'r', encoding='ascii') as file:
    for i, line in enumerate(fp):
        signatures.append(line.strip())
          
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverName, serverPort))

s.send("HELLO")

msg = s.recv(128)
print(msg.decode("utf-8"))
