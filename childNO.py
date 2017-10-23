'''
TODO make module docstring
'''
import argparse
import socket
import sys
import utilities

'''
NetworkOut
'''

def main(cmd):
    '''
    For now, main prints out that it's in childNO and then checks for the type
    '''
    print('NO')
    if utilities.check_input((str), cmd):
        return cmd
    return "error"


def network_out(host, port, message, bytecount=16):
    '''
    TODO make function docstring
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    size = len(message)
    if size < 3:
        message += ' '
        size += 1
    message_header = "Length: " + str(size +10) +"\r\n\r\n"
    original_message = message_header+message
    sock.sendall(original_message.encode())
    reply = sock.recv(16)
    reply_length = int(reply.split()[1].decode('utf-8'))
    return_message = reply
    rest = sock.recv(reply_length)
    return_message += rest
    if return_message.decode('utf-8') == original_message:
        return_message = return_message.decode('utf-8')
        print('The server said', return_message)
    else:
        print('Error:')
        print('Poor Connection with server')
    sock.close()
