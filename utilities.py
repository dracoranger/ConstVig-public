"""
utilities.py

stores any functions that should be used across all systems in a local manner
"""

#imports
import subprocess
import socket
import threading
# struct target

def parser(path, inpu):
    """
    Creator: Tate Bowers
    Input: takes in a file and its path
    Output: returns the data of that file
    This function is a Generalized parser
    sort of implemented in main, might need to differentiate someway in the future
    keeping because no real reason to remove
    """

    file = open(path+'\\'+inpu)
    use = ''
    for i in file():
        use = use + i.read
    return use


def check_input(expected, recieved):
    """
    Creator: Tate Bowers
    Input: example of the expected file type, what was recieved
    Output: whether or not the two are equal (if the file is what is expected)
    This function checks that the input matches the expected type
    generated by an explicit declairaiton of the desired system
    for example 'str' or list[]
    """
    ret = False
    #print(type(recieved))
    if isinstance(recieved, type(expected)): #== isinstance(recieved):
        ret = True

    return ret



def create_child(inp, other_arguments):
    """
    Creator: Tate Bowers
    Input: process name
    Output: connection to child input/output
    This function takes in a file to run and runs it,
    passing in the output and input to a location that you can use
    TODO figure out how to properly sync error logging
    inp

    """
    ret = -1
    if check_input('str', inp):
        if check_input('str', other_arguments): #can be a str or array, probably should be str
            run = ['python',inp+'.py',other_arguments]
            try:
                ret = subprocess.Popen(run, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    #send stdout to buffer, to write to log
            except ChildProcessError:
                print('scream and run')
                #run debug process and try again later
                #logBuffer = logBuffer + "UI Error: Failed to init"
                #try this
                    #try
                    #except ChildProcessError
                    #except as otr: again
                #seems like it would be a good idea to push this to a function.
            #except:
                #something else went wrong, try to make better
                #logBuffer=logBuffer+"UI Error: " + sys.exc_info()[0]#think this is the syntax

    return ret

def comm_out(data,sock):
    """
    Creator: Tate Bowers
    Input: port number, string of data
    Output: none
    This function sends a piece of data to a given port
    """
    #network_out('localhost', port, data)
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect(('127.0.0.1', port))
    sock.send(data.encode())
    #server_thread = threading.Thread(target=readFromServer, args=([sock]))
    #return server_thread, clientSocket


def comm_in(port):
    """
    Creator: Tate Bowers
    Input: port number
    Output: a persistent socket maintained by a thread, the socket
    This function returns a listener as a thread
    """
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.bind(('127.0.0.1', port))
    clientSocket.listen(10000)
    server_thread = threading.Thread(target=readFromServer, args=([clientSocket]))
    return server_thread, clientSocket

def readFromServer(sock):
    while True:
        buf = sock.recv(1024).decode()
        print(buf)

def network_out(host, port, exploit):
    """
    TODO make function docstring
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    size = len(exploit)
    if size < 3:
        exploit += ' '
        size += 1
    exploit_header = "Length: " + str(size +10) +"\r\n\r\n"
    original_exploit = exploit_header+exploit
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

def network_in(host, port):
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
