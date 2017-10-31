'''
NetIn
'''

import socket
import sys
import utilities

def main():
    '''
    Checks for type and returns the input, otherwise returns an error message
    '''
    keep_going = True
    listener, sock = utilities.comm_in(9751)
    while keep_going:
        #commented out print() and changed input()
        #print('NI')
        #try:
        able = 'Temp val'#sys.stdin.readline(5)
        if utilities.check_input((bytes), able):
            utilities.comm_out(able, 15551)
        #except EOFError:
        #    print('no data supplied')
    sock.close()
    listener.join()



def net_in(host, port):
    '''
    TODO fill in docstring
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    #sock.connect((host, port))
    #sock.shutdown(socket.SHUT_WR)
    received = 0
    while True:
        print('Listening at', sock.getsockname())
        soc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('Socket connects', soc.getsockname(), 'and', soc.getpeername())
        message = soc.recv(16)
        message_length = int(message.split()[1].decode('utf-8'))
        return_message = message
        rest = soc.recv(message_length)
        return_message += rest
        print_message = return_message.decode('utf-8')
        print('The incoming sixteen-octet message says', print_message)
        soc.sendall(return_message)
        soc.close()
        print('  Reply sent, socket closed\n')

main()
