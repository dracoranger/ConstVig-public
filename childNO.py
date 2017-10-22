import argparse, socket, sys, utilities

'''
NetworkOut
'''

def main(cmd):
    if check_input((str), cmd):
        return cmd
else:
        return "error"


def NetworkOut(host, port, bytecount=16, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = data.encode()  # need to convert to byte
    bytecount = (len(message) + 15) // 16 * 16  # round up to a multiple of 16
    sock.connect((host, port))
    sent = 0
    while sent < bytecount:
        sock.sendall(message)
        sent += len(message)
        print('\r  %d bytes sent' % (sent,), end=' ')
        sys.stdout.flush()
    print()
    sock.shutdown(socket.SHUT_WR)
    sock.close()
