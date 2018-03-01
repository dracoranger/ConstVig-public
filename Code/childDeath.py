""" handles the user interface

Classes: None
Exceptions:
Functions:
main --
"""

import utilities
import sys
import socket

def main():
    """
    For now, this just asserts what child is being used and checks for the type
    """
    keep_going = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 15551))
    recieved = sock.recv(1024).decode()
    #listener, sock = utilities.comm_in(9751)

    able = bytes('Temp val', 'utf-8')
    if utilities.check_input((bytes), able):
        sock.send(able.encode())
    sock.close()
main()
