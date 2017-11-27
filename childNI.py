""" handles incoming network traffic

Classes: None
Exceptions:
Functions:
main --
net_in --
"""

import socket
import sys
import utilities
from scapy.all import *

def main():
    """
    Checks for type and returns the input, otherwise returns an error message
    """
    keep_going = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 15551))
    recieved = sock.recv(1024).decode()
    #listener, sock = utilities.comm_in(9751)
    while keep_going:
        #commented out print() and changed input()
        #print('NI')
        #try:
        able = bytes('Temp val', 'utf-8')#sys.stdin.readline(5)
        if utilities.check_input((bytes), able):
            sock.send(able.encode())
            #utilities.comm_out(able, sock)
        #except EOFError:
        #    print('no data supplied')
    sock.close()
    #listener.join()



def net_in(host, port):
    """
    TODO fill in docstring
    """
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

#scapy

def analyzer(inp):
    '''
        >>>analyzer()
        return [80[n, n+20, n+40, n+80, n+100],7558[n+5,n+10,n+15],...],[jklasdnvhiuopq[n, n+20, n+40, n+80, n+100],qiuopnjvpasewrnjkaxpjbnadfsjiopea[n+5,n+10,n+15],...]
    '''
    ports, timestamp, data = parser(inp)

    ret = analyzer_ports(ports,timestamp)
    ret = ret + analyzer_data(data,timestamp)

def analyzer_data(dat, timestamp):
    '''
        >>>analyzer_data()
        [jklasdnvhiuopq[n, n+20, n+40, n+80, n+100],qiuopnjvpasewrnjkaxpjbnadfsjiopea[n+5,n+10,n+15],...]
    '''

def analyzer_ports(ports, timestamp):
    '''
        >>>analyzer_ports()
        [80[n, n+20, n+40, n+80, n+100],7558[n+5,n+10,n+15],...]
    '''

def parser(inp):
    '''
        >>>parser()
        [80,7558,7558,80,7558,80,7558...],[n, n+5,n+10,n+15,n+20,n+40,n+80],[jklasdnvhiuopq,qiuopnjvpasewrnjkaxpjbnadfsjiopea,qiuopnjvpasewrnjkaxpjbnadfsjiopea,qiuopnjvpasewrnjkaxpjbnadfsjiopea,jklasdnvhiuopq,jklasdnvhiuopq]
    '''
