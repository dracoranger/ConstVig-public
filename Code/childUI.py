# handles the user interface

# NAME: Child User Interface
# FILE: ConstVig/Code/childUI.py
# CLASSES: N/A
# EXCEPTIONS:
# FUNCTIONS:
#     main


import sys
import socket

import utilities


def main():
    #For now, asserts what child is being used and checks for the type
    keep_going = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 15550))
    recieved = sock.recv(1024).decode()
    #listener, sock = utilities.comm_in(9751)
    while keep_going:
        able = bytes('Temp val', 'utf-8')
        if utilities.check_input((bytes), able):
            sock.send(able.encode())
    sock.close()


main()
