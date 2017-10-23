import argparse, socket, sys, utilities

'''
NetworkOut
'''

def main(cmd):
    if utilities.check_input((str), cmd):
        return cmd
    else:
        return "error"


def NetworkOut(host, port, bytecount=16, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    size=len(message)
    if size < 3:
        message+=' '
        size+=1
    messageHeader = "Length: " + str(size +10) +"\r\n\r\n"
    originalMessage = messageHeader+message
    sock.sendall(originalMessage.encode())
    reply = sock.recv(16)
    replyLength = int(reply.split()[1].decode('utf-8'))
    returnMessage = reply
    rest = sock.recv(replyLength)
    returnMessage += rest
    if returnMessage.decode('utf-8') == originalMessage:
        returnMessage = returnMessage.decode('utf-8')
        print('The server said', returnMessage)
    else:
        print('Error:')
        print('Poor Connection with server')
    sock.close()
