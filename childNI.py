'''
NetIn
'''
import socket, sys
import socket, sys, utilities

def main(cmd):
    if utilities.check_input((str), cmd):
        return cmd
    else:
        return "error"


def networkIn(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((host,port))
    sock.listen(1)
    #sock.connect((host, port))
    #sock.shutdown(socket.SHUT_WR)
    received = 0
    while True:
        print('Listening at', sock.getsockname())
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('Socket connects', sc.getsockname(), 'and', sc.getpeername())
        message = sc.recv(16)
        messageLength = int(message.split()[1].decode('utf-8'))
        returnMessage = message
        rest = sc.recv(messageLength)
        returnMessage += rest
        printMessage = returnMessage.decode('utf-8')
        print('The incoming sixteen-octet message says', printMessage)
        sc.sendall(returnMessage)
        sc.close()
        print('  Reply sent, socket closed\n')
