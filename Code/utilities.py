"""stores any functions that should be used across all systems in a local manner

Classes: None
Exceptions:
Functions:
parser -- parses data from files
check_input -- checks whether the input is of the correct type
create_child -- runs the file (will be a child process) given as input
comm_out -- sends communications out through ports
comm_in -- creates a listener
read_from_server -- prints messages received from server
network_out -- actual process for outgoing network communications
network_in -- actual process for incoming network communications
"""

import subprocess
import socket
import threading
import os
import configparser
# struct target

def parser(path, inpu):
    """parses a file

    Summary of behavior: A generalized parser (partially implemented in main)
	Arguments: a file and its path
    Return values: the data of the input file
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called:
    Creator: Tate Bowers

    keeping for future potential use
    """

    file = open(path+'\\'+inpu)
    use = ''
    for i in file():
        use = use + i.read
    return use


def check_input(expected, recieved):
    """checks whether input is of the expected type.

    Summary of behavior: Checks that the received input type matches
        the type that was expected (which is explicitly given in the input. For example, received "hello world" with type int would return false.
	Arguments: the type that is expected and what was actually receieved
    Return values: boolean stating whether the input types matched
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called:
    Creator: Tate Bowers
    """
    ret = False
    #print(type(recieved))
    if isinstance(recieved, type(expected)): #== isinstance(recieved):
        ret = True

    return ret



def create_child(fileName, other_arguments):
    """ creates a child that is given in fileName.

    Summary of behavior: Runs the input file, passing the input and output to a location that is useable
	Arguments: process name (a file) and any flags
    Return values: exit code
    Side effects: a connection to child input/output is made
    Exceptions raised:
    Restrictions on when it can be called:
    Creator: Tate Bowers

    TODO figure out how to properly sync error logging
    inp
    """
    ret = -1
    if check_input('str', fileName):
        if check_input('str', other_arguments): #can be a str or array, probably should be str
            run = ['python', fileName+'.py', other_arguments]
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

def create_child_gen(run):
    """ creates a child that is given in fileName.
        Same as above except can run more than python files
        depends on user properly uploading a run[] with the reuqired arguements
    """
    ret = -1
    temp = ''
    if check_input(temp, run):
        try:
            ret = subprocess.Popen(run, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

                #should run to completion, probably should pipe output to a log file
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

def comm_out(data, sock):
    """handles data to be sent out over the network

    Summary of behavior:
	Arguments: string of data to be sent and the desired port number
    Return values: None
    Side effects: Data sent to the given port
    Exceptions raised:
    Restrictions on when it can be called:
    Creator: Tate Bowers
    """

    #network_out('localhost', port, data)
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect(('127.0.0.1', port))
    sock.send(data.encode())
    #server_thread = threading.Thread(target=read_from_server, args=([sock]))
    #return server_thread, client_socket


def comm_in(port):
    """handles data coming in from the network

    Summary of behavior:
	Arguments: the desired port
    Return values: A listener as a thread
    Side effects: A persistent socket is maintained by a thread, the socket
    Exceptions raised:
    Restrictions on when it can be called:
    Creator: Tate Bowers
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('127.0.0.1', port))
    client_socket.listen(10000)
    server_thread = threading.Thread(target=read_from_server, args=([client_socket]))
    return server_thread, client_socket

def read_from_server(sock):
    """reads messages from the server and prints them"""
    while True:
        buf = sock.recv(1024).decode()
        print(buf)

def network_out(host, port, exploit):
    """function that actually communicates with the network

    Summary of behavior: Sends out exploits over the network
	Arguments: the target host, port, and exploit to be sent
    Return values: None
    Side effects: the input (an exploit, hopefully) is sent over the network to a specific host.
    Exceptions raised:
    Restrictions on when it can be called:
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
    """function that directly handles incoming network traffic

    Summary of behavior: takes messages from the network and prints them out, along with other relevant information
	Arguments: the host and port
    Return values: None
    Side effects: print messages and accepted port connections
    Exceptions raised:
    Restrictions on when it can be called:
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

def generateDefaultConfig():
    config = configparser.ConfigParser()
    config['Main'] = {'Rounds' : '100',
                      'Round length':'300'

                    }
    config['NetworkIn'] = {

                        }
    config['NetworkOut'] = {
                        '#The range of IPs that should be targeted should be in the format XXX.XXX.XXX.XXX/XX with the first IP and the subnet mask':'',
                        'ipRange':'192.168.1.0/24',
                        '# Sepirate the ports to be attacked with a ,':'',
                        'ports': '23,24,35',
                        'SUBMIT_FLAG_IP':'192.168.1.1',
                        'SUBMIT_FLAG_PORT':'9001',
                        '#Both of these are the defaults, it grabs the current working directory when it is run, then appends chaff and attack.':'',
                        'PATH_CHAFF':os.getcwd()+'\\chaff',
                        'PATH_ATTACK':os.getcwd()+'\\attacks'
                        }
    config['Attacks'] = {
                        '#Format should be the file name followed by the command line arguement to run it.\n#Store the attacks in the PATH_ATTACK directory\n#add -i to have it iterate through the items in ipRange\n#add -p to iterate through the ports\n#add -f to add the ip address and port of where the flag should be submitted in the format SUBMIT_FLAG_IP + \' \' + SUBMIT_FLAG_PORT':'',
                        "hello_world.py" : "python hello_world.py",
                        "looper.py" : "python looper.py"
                        }
    config['Chaff'] = {
                        '#Format should be the file name followed by the command line arguement to run it.\n#Store the chaff in the PATH_CHAFF directory\n#add -i to have it iterate through the items in ipRange\n#add -p to iterate through the ports\n#add -f to add the ip address and port of where the flag should be submitted in the format SUBMIT_FLAG_IP + \' \' + SUBMIT_FLAG_PORT':'',

                    }
    with open('constvig.conf','w') as configfile:
        config.write(configfile)

def parseConfig(section):
    config = configparser.ConfigParser()
    #taken from python.org wiki
    def configSectionMap(section):

        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    config.read('constvig.conf')
    ret = configSectionMap(section)
    return ret

def submit_flag(ip, port, data):
    return "welp"
