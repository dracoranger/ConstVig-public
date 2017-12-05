import socket
import argparse



def server(host, port):
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


def client(host, port, pcap):
    """ TODO -- include the one line summary
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    size = len(pcap)
    if size < 3:
        pcap += ' '
        size += 1
    exploit_header = "Length: " + str(size +10) +"\r\n\r\n"
    original_exploit = exploit_header+pcap
    sock.sendall(original_exploit.encode())
    reply = sock.recv(16)
    reply_length = int(reply.split()[1].decode('utf-8'))
    return_exploit = reply
    rest = sock.recv(reply_length)
    return_exploit += rest
    if return_exploit.decode('utf-8') == original_exploit:
        return_exploit = return_exploit.decode('utf-8')
        print('The server said', return_exploit)
    else:
        print('Error:')
        print('Poor Connection with server')
    sock.close()

def random_msg():
    size = random.randint(1,3)
    messageHeader = "Length: " + str(size +10) +"\r\n\r\n"
    messageBody = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(size)])
    message = messageHeader + messageBody
    return message.encode('ascii')

if __name__=='__main__':
    parser - argparse.ArgumentParser(description='Client/Server')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-s',metavar='server',help='Server')
    parser.add_argument('-c',metavar='client',help='cliet')
    parser.add_argument('-p', metavar='port',type=int,default=1060,
                        help='TCP Port (default 1060)')
    args = parser.parser()
    msg=random_msg()
    print(args)