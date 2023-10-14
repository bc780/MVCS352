import socket, sys

#take in arguments
serverName = sys.argv[1]
serverPort = sys.argv[2]
msgName = sys.argv[3]
sigName = sys.argv[4]

#temp debug to check args
print(serverName)
print(serverPort)
print(msgName)
print(sigName)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverName, serverPort))