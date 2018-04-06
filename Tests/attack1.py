from socket import *
import threading
import sys
import base64

connect = True
serverName = '127.0.0.1'
serverPort = 9001 #not correct

#http://www.binarytides.com/raw-socket-programming-in-python-linux/
send = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
send.connect((serverName, serverPort))

message = 'Drake has joined!!'
print(message)
#send.send(message.encode())

buff = send.recv(1024).decode()
print(buff)
buff = base64.b64encode(buff)#decryptor.update(buff)
print(buff)
#print(buff.decode())
#buff = decryptor.update(buff) + decryptor.finalize()

print("Shutdown complete... exiting")
sys.exit()
