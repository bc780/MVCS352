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

# temp debug
# print(keys)
# print(type(keys[0]))

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
if msg.decode("ascii") == "HELLO":
    c.send("260 OK".encode("ascii"))
    print("260 OK\n")
    while True:
        msg = c.recv(1028)
        print(msg.decode("ascii")+ "\n")
        if msg.decode("ascii") == "DATA":
            msg = c.recv(10000)
            tempStr = msg.decode("ascii")
            print(tempStr + "\n")
            
            #unescape the line here
            tempStr = tempStr.replace("\.",".")
            #temp debug
            # print(tempStr + "\n")
            
            #use sha256 hash here
            hash = hashlib.sha256()
            hash.update(tempStr.encode("ascii"))
            hash.update(keys[i].encode("ascii"))
            i += 1

            c.send("270 SIG".encode("ascii"))
            print("270 SIG\n")
            c.send(hash.hexdigest().encode("ascii"))
            print(hash.hexdigest() + "\n")
            #send back sig
            msg = c.recv(1028)
            print(msg.decode("ascii")+ "\n")
            if msg.decode("ascii") == "PASS":
                c.send("260 OK".encode("ascii"))
                print("260 OK\n")
            elif msg.decode("ascii") == "FAIL":
                c.send("260 OK".encode("ascii"))
                print("260 OK\n")
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
