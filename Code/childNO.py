""" handles traffic leaving to the rest of the network

Classes: None
Exceptions:
Functions:
main -- TBA
network_out --
"""

import argparse
import socket
import sys
import utilities
import os

"""
NetworkOut
"""

#Constants or user set variables

#Path variables
#os.path.dirname(os.path.realpath(__file__)) or os.getcwd()
#https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
PATH_ATTACK = os.getcwd()+'\\attacks'
PATH_CHAFF = os.getcwd()+'\\chaff'

# filename : running arugments stored as a list
attackDictionary = {


}
attackOrder=[]
chaffDictionary = {


}
chaffOrder=[]
#generates attackDictionary
#generates order
def iter_thru_attack_config(filename):
    fil = open(filename)

def run_attacks():
    directory = os.fsencode(PATH_ATTACK)
    attackStorage=[] #inefficent as heck.  Not sure how else to guarentee aphebetical and no duplicates
    for fil in os.listdir(directory):
        filename = os.fsdecode(fil)
        attack = utilities.create_child(attackDictionary[filename])
        attackStorage.append(attack)
        attackOrder.append(filename)
    currNum=0
    for attack in attackStorage:
        if attack.process.poll() == 0: #think this should work.  Not sure since not a child class.  Might just be process.poll
            print('success')
            #push to logfile success
        elif isinstance(attack.process.poll(), type(None)):
            print(attackOrder[currNum]+' on going')
        else:
            print(attackOrder[currNum]+attack.process.stderr)
        currNum=currNum+1

def main():
    """[prints out childNO and then] checks for the type

    Summary of behavior:
    Arguments: None
    Return values:
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called:
    """
    keep_going = True
    while keep_going:
        #commented out the print() and input()
        #print('NO')
        able = sys.stdin.readline(5)
        if utilities.check_input((str), able):
            print(able)


def network_out(host, port, exploit):
    """ TODO -- include the one line summary

    Summary of behavior:
    Arguments:
    Return values:
    Side effects:
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


main()
