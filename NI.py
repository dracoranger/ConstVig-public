import socket
import argparse
import random
import string

class tcp(object):
    def __init__(self,role,host,p,msg):
        self.mode=role
        self.host=host
        self.port=p
        self.msg=msg
        if self.mode  == 's':
            self.server(self.host,self.port)
        else:
            self.client(self.host,self.port,self.msg)


    def server(self,host, port):
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
            #return_message = message
            rest = soc.recv(message_length)
            return_message = rest.split(2)
            #print_message = return_message.decode('utf-8')
            with open('test.pcap','wb') as w:
                w.write(return_message)
            print('Recieved new capture!')#print('The incoming sixteen-octet message says', print_message)
            ms = '\nGot The Message!!!'
            soc.sendall(ms.encode())
            soc.close()
            print('  Reply sent, socket closed\n')


    def client(self,host, port, pcap):
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
        return_exploit = reply
        print('The server said:\n', return_exploit.decode('utf-8'))
        sock.close()

def random_msg():
    with open(r'C:\Users\x86075\Documents\Firstie Year\IT401\Sprint2\17-36.pcap','rb') as read:
        lines = read.readlines()
        part = b''
        for line in lines[:10]:
            part+=line
    size = len(part)#random.randint(17000,21000)
    print(size)
    messageHeader = "Length: " + str(size +10) +"\r\n\r\n"
    messageBody = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(size)])
    message = messageHeader.encode() + part#messageBody
    return message#.encode('ascii')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Client/Server')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('role',
                        help="'c' for client, 's' for server")
    parser.add_argument('-p', metavar='port',type=int,default=1060,
                        help='TCP Port (default 1060)')
    args = parser.parse_args()
    args=vars(args)
    msg=random_msg()
    role = args['role']
    host = args['host']
    port = args['p']
    if role == 'c' or role == 's':
        comm=tcp(role,host,port,msg)
    else:
        print('Your role is incorrect!')
        print("You must enter 'c' for client or 's' for server")
