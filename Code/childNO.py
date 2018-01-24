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
chaffDictionary = {


}

#generalized version of below
def iter_thru_config(which, dicti):
    #which is either "Attack" or "Chaff"
    diction = utilities.parseConfig(which)
    for i in diction:
        if not i in dicti:
            #dicti is either chaff or attack dictionary
            dicti[i] = diction[i]

def run_processes(which, dicti, path):
    #which is either "Attack" or "Chaff"
    iter_thru_config(which, dicti)
    #either PATH_ATTACK or PATH_CHAFF
    directory = os.fsencode(path)
    launchStorage = [] #inefficent as heck.  Not sure how else to guarentee aphebetical and no duplicates
    launchOrder = []
    for fil in os.listdir(directory):
        filename = os.fsdecode(fil)
        #print(attackDictionary)
        run = dicti[filename]
        run = run.replace(filename, PATH_ATTACK+'\\'+filename)
        launch = utilities.create_child_gen(run)
        launchStorage.append(launch)
        launchOrder.append(filename)

    complete = False
    while not complete:
        #might want to create an escape which kills an indefinitely running process
        currNum = 0
        time.sleep(3)
        complete = True
        for launch in launchStorage:
            if utilities.check_input(launch.poll(),1):
                if launch.poll() == 0: #think this should work.  Not sure since not a child class.  Might just be process.poll
                    print(str(launchOrder[currNum]) + ' success: '+str(launch.poll()))
                    #push to logfile success
                else:
                    print(str(launchOrder[currNum])+ str(launch.poll()))#+attack.process.stderr)
            elif isinstance(launch.poll(), type(None)):
                print(launchOrder[currNum]+' on going')
                complete = False
            currNum = currNum+1

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
    attackOrder = []
    for fil in os.listdir(directory):
        filename = os.fsdecode(fil)
        run = attackDictionary[filename]
        run = run.replace(filename, PATH_ATTACK+'\\'+filename)
        attack = utilities.create_child_gen(run)
        attackStorage.append(attack)
        attackOrder.append(filename)

    complete = False
    while not complete:
        #might want to create an escape which kills an indefinitely running process
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
    # use generalized
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
    #Either preferences in main or here
    #read_preferences()
    #which, dicti, path
    run_processes("Chaff",chaffDictionary,PATH_CHAFF)
    run_processes("Attacks",attackDictionary,PATH_ATTACK)
    run_processes("Chaff",chaffDictionary,PATH_CHAFF)
        #commented out the print() and input()
        #print('NO')
main()
