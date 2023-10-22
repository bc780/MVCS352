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
print("HELLO\n")

msg = s.recv(128)
print(msg.decode("ascii")+ "\n")
if msg.decode("ascii") != "260 OK":
    print("error: expected 260 OK")
    exit()

for i in range(len(msgBytes)):

    tempStr = msgBytes[i].decode()
    print(tempStr)
    tempStr = tempStr.replace(".","\.")
    s.send("DATA".encode("ascii"))
    print("DATA\n")        
    s.send(tempStr.encode("ascii"))
    print(tempStr + "\n")

    msg = s.recv(128)
    print(msg.decode("ascii")+ "\n")
    if msg.decode("ascii") != "270 SIG":
        print("error: expected 270 SIG")
        exit()

    msg = s.recv(10000)
    print(msg.decode("ascii")+ "\n")

    #compare signature strings here

    if signatures[i] == msg.decode("ascii"):
        s.send("PASS".encode("ascii"))
        print("PASS\n")
    else:
        s.send("FAIL".encode("ascii"))
        print("FAIL\n")
    msg = s.recv(128)
    print(msg.decode("ascii")+ "\n")
    if msg.decode("ascii") != "260 OK":
        print("error: expected 260 OK")
        exit()
s.send("QUIT".encode("ascii"))
print("QUIT\n")
s.close()
