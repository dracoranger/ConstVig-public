# handles traffic leaving to the rest of the network

# NAME: Child Network In
# FILE: ConstVig/Code/childNO.py
# CLASSES: N/A
# EXCEPTIONS:
# FUNCTIONS:
#   main
#   iter_thru_config
#   run_processes

import os
import time
import ipaddress
import utilities

#Constants or user set variables

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
        if '-f' in run:
            run = run.replace('-f', '-f ' + SUBMIT_FLAG_IP + ','+ SUBMIT_FLAG_PORT)

        temp = run

        if '-ip' in temp and '-p' in temp:
            for p in PORTS:
                for i in IP_RANGE:
                    temp = run.replace('-ip', '-ip ' + str(i))
                    temp = temp.replace('-p','-p ' + str(p))
                    launch = utilities.create_child_gen(temp)
                    launchStorage.append(launch)
                    launchOrder.append(filename)
        elif '-ip' in temp:
            for i in IP_RANGE:
                temp = run.replace('-ip', '-ip ' + str(i))
                launch = utilities.create_child_gen(temp)
                launchStorage.append(launch)
                launchOrder.append(filename)
        elif '-p' in temp:
            for p in PORTS:
                temp = run.replace('-p','-p ' + str(p))
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
            if utilities.check_input(launch.poll(), 1):
                if launch.poll() == 0:
                    response = str(launch.communicate())
                    #COMMENT OUT THIS LINE TO NOT SUBMIT THE FLAG BASED ON WHATEVER IS SENT TO STDOUT
                    utilities.submit_flag(SUBMIT_FLAG_IP, SUBMIT_FLAG_PORT, response)
                    #TODO, make sure this is correct
                    with open(log, 'a') as logpointer:
                        logpointer.write('%s success: %s\n' % (str(launchOrder[currNum]), response))
                    remove.append(launch)
                    #push to logfile success
                else:
                    response = str(launch.communicate())
                    with open(log, 'a') as logpointer:
                        logpointer.write(str(launchOrder[currNum]) + ' failure: '+response+ '\n')
                    print(str(launchOrder[currNum])+ str(launch.communicate()))#+attack.process.stderr)
                    remove.append(launch)
            elif isinstance(launch.poll(), type(None)):
                print(launchOrder[currNum]+' on going')
                complete = False
            currNum = currNum+1
        for i in remove:
            temp = launchStorage.index(i)
            launchStorage.remove(i)
            launchOrder.pop(temp)

def main():
    #[prints out childNO and then] checks for the type

    #Summary of behavior:
    #Arguments: None
    #Return values:
    #Side effects:
    #Exceptions raised:
    #Restrictions on when it can be called:

    attackDictionary = {
    }
    chaffDictionary = {
    }
    #Either preferences in main or here
    #read_preferences()
    #which, dicti, path
    run_processes("Chaff", chaffDictionary, PATH_CHAFF, "chaff.log")
    run_processes("Attacks", attackDictionary,PATH_ATTACK, "attack.log")
        #commented out the print() and input()
        #print('NO')
main()
