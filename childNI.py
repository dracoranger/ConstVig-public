'''
NetIn
'''
import socket, sys, utilities

def main(cmd):
    print('NI')
    if utilities.check_input((str), cmd):
        return cmd
    else:
        return "error"


def networkIn(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    #sock.shutdown(socket.SHUT_WR)
    received = 0
    while True:
        data = sock.recv(42) #decode('utf-8')
        if not received:
            print('  The first data received says', repr(data))
        if not data:
            break
        received += len(data)
        print('\r  %d bytes received' % (received,), end=' ')

    print()
    sock.close()
