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
import string
import os
import time
import utilities



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
def iter_thru_attack_config():
    diction = utilities.parseConfig('Attacks')
    for i in diction:
        if not i in attackDictionary:
            attackDictionary[i] = diction[i]

def run_attacks():
    iter_thru_attack_config()
    directory = os.fsencode(PATH_ATTACK)
    attackStorage = [] #inefficent as heck.  Not sure how else to guarentee aphebetical and no duplicates
    for fil in os.listdir(directory):
        filename = os.fsdecode(fil)
        run = attackDictionary[filename]
        run = run.replace(filename, PATH_ATTACK+'\\'+filename)
        attack = utilities.create_child_gen(run)
        attackStorage.append(attack)
        attackOrder.append(filename)

    complete = False
    while not complete:
        currNum = 0
        time.sleep(3)
        complete = True
        for attack in attackStorage:
            if utilities.check_input(attack.poll(),1):
                if attack.poll() == 0: #think this should work.  Not sure since not a child class.  Might just be process.poll
                    print(str(attackOrder[currNum]) + ' success')
                    #push to logfile success
                else:
                    print(attackOrder[currNum])#+attack.process.stderr)
            elif isinstance(attack.poll(), type(None)):
                print(attackOrder[currNum]+' on going')
                complete = False
            currNum = currNum+1


def run_chaff():
    return "incomplete"

def main():
    """[prints out childNO and then] checks for the type

    Summary of behavior:
    Arguments: None
    Return values:
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called:
    """
    #loop through on a user-established timer interval
    run_attacks()
        #commented out the print() and input()
        #print('NO')
