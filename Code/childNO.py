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
import ipaddress
import utilities



"""
NetworkOut
"""

#Constants or user set variables

#Path variables
#os.path.dirname(os.path.realpath(__file__)) or os.getcwd()
#https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
dictionA = utilities.parseConfig('Attacks')
dictionC = utilities.parseConfig('Chaff')
dictionNO=utilities.parseConfig('NetworkOut')
PATH_ATTACK = dictionNO['path_attack']
PATH_CHAFF = dictionNO['path_chaff']
IP_RANGE =  list(ipaddress.ip_network(dictionNO['iprange']).hosts())
PORTS = dictionNO['ports'].split(',')
SUBMIT_FLAG_PORT = dictionNO['submit_flag_port']
SUBMIT_FLAG_IP = dictionNO['submit_flag_ip']

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

def run_processes(which, dicti, path, log):
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
        #allow replacement of IP and Ports accessed
        #might chose how flag is sent.
        if not run.find('-f') == -1:
            temp.replace('-f', SUBMIT_FLAG_IP + ' '+ SUBMIT_FLAG_PORT)
        if not run.find('-i') == -1 and not run.find('-p') == -1:
            for p in PORTS:
                for i in IP_RANGE:
                    temp = run
                    temp.replace('-i',str(i))
                    temp.replace('-p',p)
                    launch = utilities.create_child_gen(temp)
                    launchStorage.append(launch)
                    launchOrder.append(filename)
        elif not run.find('-i') == -1:
            for i in IP_RANGE:
                temp = run
                temp.replace('-i',str(i))
                launch = utilities.create_child_gen(temp)
                launchStorage.append(launch)
                launchOrder.append(filename)
        elif not run.find('-p') == -1:
            for p in PORTS:
                temp = run
                temp.replace('-p',p)
                launch = utilities.create_child_gen(temp)
                launchStorage.append(launch)
                launchOrder.append(filename)
        else:
            launch = utilities.create_child_gen(run)
            launchStorage.append(launch)
            launchOrder.append(filename)
    complete = False
    while not complete:
        #might want to create an escape which kills an indefinitely running process
        remove = []
        currNum = 0
        time.sleep(3)
        complete = True
        for launch in launchStorage:
            if utilities.check_input(launch.poll(),1):
                if launch.poll() == 0: #think this should work.  Not sure since not a child class.  Might just be process.poll
                    response = str(launch.communicate())
                    #automatically submit flag?
                    #probably a good idea
                    #COMMENT OUT THIS LINE TO NOT SUBMIT THE FLAG BASED ON WHATEVER IS SENT TO STDOUT
                    utilities.submit_flag(SUBMIT_FLAG_IP,SUBMIT_FLAG_PORT,response)
                    log = open(log, 'a')
                    log.write(str(launchOrder[currNum]) + ' success: '+response+ '\n')
                    log.close()
                    #print(str(launchOrder[currNum]) + ' success: '+str(launch.communicate()))
                    remove.append(launch)
                    #push to logfile success
                else:
                    response = str(launch.communicate())
                    log = open(log, 'a')
                    log.write(str(launchOrder[currNum]) + ' success: '+response+ '\n')
                    log.close()
                    print(str(launchOrder[currNum])+ str(launch.communicate()))#+attack.process.stderr)
            elif isinstance(launch.poll(), type(None)):
                print(launchOrder[currNum]+' on going')
                complete = False
            currNum = currNum+1
        for i in remove:
            temp = launchStorage.index(i)
            launchStorage.remove(i)
            launchOrder.pop(temp)

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
    run_processes("Chaff",chaffDictionary,PATH_CHAFF, 'chaff.log')
    run_processes("Attacks",attackDictionary,PATH_ATTACK, 'attack.log')
    run_processes("Chaff",chaffDictionary,PATH_CHAFF, 'chaff.log')
        #commented out the print() and input()
        #print('NO')
main()
