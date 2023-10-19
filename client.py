import socket, sys

#take in arguments
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
msgName = sys.argv[3]
sigName = sys.argv[4]

#temp debug to check args
# print(serverName)
# print(serverPort)
# print(msgName)
# print(sigName)

msgSizes = []
msgBytes = []
signatures = []

with open(msgName, 'r', encoding='ascii') as file:
    for i, line in enumerate(file):
        if i%2==0:
            msgSizes.append(int(line.strip()))
        else:
            tempBytes = bytes(line.strip(),'ascii')
            msgBytes.append(tempBytes) 
          
with open(sigName, 'r', encoding='ascii') as file:
    for i, line in enumerate(file):
        signatures.append(line.strip())
          
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverName, serverPort))

s.send("HELLO".encode("ascii"))

msg = s.recv(128)
if msg.decode("ascii") != "260 OK":
    print("error: expected 260 OK")
    exit()

for i in msgSizes:

    # escape the message here
    escapedMsg = msgBytes[i]
    for char in temp:
        if char == 34:
            escapedMsg[i] = 92
            i += 1
            escapedMsg[i] = 34
            i += 1
            j += 1
        else:
            escapedMsg[i] = msgBytes[j]
            i += 1
            j += 1
    s.send("DATA".encode("ascii"))        
    s.send(escapedMsg.encode("ascii"))

    msg = s.recv(128)
    if msg.decode("ascii") != "270 SIG":
        print("error: expected 270 SIG")
        exit()

    msg = s.recv(10000)

    #compare signature strings here

    if signatures[i] == msg:
        s.send("PASS".encode("ascii"))
    else:
        s.send("FAIL".encode("ascii"))
    msg = s.recv(128)
    if msg.decode("ascii") != "260 OK":
        print("error: expected 260 OK")
        exit()
s.send("QUIT").encode("ascii")
s.close()
