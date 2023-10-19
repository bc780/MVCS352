from fileinput import filename
import socket, sys, hashlib

# take in arguments
listenPort = int(sys.argv[1])
keyName = sys.argv[2]

#temp debug to check args
# print(listenPort)
# print(keyName)

keys = []

with open(keyName, 'r', encoding='ascii') as file:
    for i, line in enumerate(file):
        keys.append(line.strip())
#tracker for what key its on        
i = 0
#establish socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', listenPort))
s.listen(5)

#listen for connection
c, address = s.accept()
msg = c.recv(1028)
print(msg.decode("ascii")+ "\n")
print(msg.decode("ascii"))
if msg.decode("ascii") == "HELLO":
    c.send("260 OK".encode("ascii"))
    while True:
        msg = c.recv(1028)
        print(msg.decode("ascii")+ "\n")
        if msg.decode("ascii") == "DATA":
            msg.recv(10000)
            print(msg.decode("ascii")+ "\n")
            
            #unescape the line here
            msg = msg.replace("\\.",".")
            
            #use sha256 hash here
            hash = hashlib.sha256()
            hash.update(msg.encode("ascii"))
            hash.update(keys[i].encode("ascii"))
            i += 1

            c.send("270 SIG".encode("ascii"))
            c.send(hash.hexdigest())
            #send back sig
            msg.recv(1028)
            print(msg.decode("ascii")+ "\n")
            if msg.decode("ascii") == "PASS":
                c.send("260 OK".encode("ascii"))
            elif msg.decode("ascii") == "FAIL":
                c.send("260 OK".encode("ascii"))
            else:
                print("error: illegal command, expecting PASS or FAIL")
                c.close()
                break
        elif msg.decode("ascii") == "QUIT":
            c.close()
            break
        else:
            print("error: illegal command, expecting DATA or QUIT")
            c.close()
            break
else:
    print("error: illegal command, expecting HELLO")
    c.close()
