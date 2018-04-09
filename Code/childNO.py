# handles traffic leaving to the rest of the network

# NAME: Child Network Out
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
import queue
import subprocess
import utilities
import threading
import ssResponse as sub


# Constants & user set variables (naming exception made for variables)
dictionA = utilities.parse_config('Attacks')
dictionC = utilities.parse_config('Chaff')
dictionNO = utilities.parse_config('NetworkOut')
PATH_ATTACK = dictionNO['path_attack']
PATH_CHAFF = dictionNO['path_chaff']
IP_RANGE =  dictionNO['iprange'].split(',')
PORTS = dictionNO['ports'].split(',')
SUBMIT_FLAG_PORT = dictionNO['submit_flag_port']
SUBMIT_FLAG_IP = dictionNO['submit_flag_ip']


def iter_thru_config(which, dicti):
    # "which" is either "Attack" or "Chaff"
    diction = utilities.parse_config(which)
    for i in diction:
        if not i in dicti:
            # dicti is either chaff or attack dictionary
            dicti[i] = diction[i]

def ip(ipRange):
    try:
        for i in ipRange:
            if ipaddress.ip_address(i):
                continue
        return True
    except ValueError:
        return False


def run_processes(which, dicti, path, log):
    # "which" is either "Attack" or "Chaff"
    iter_thru_config(which, dicti)
    range=ip(IP_RANGE)
    if range is False:
        return "Fix IP Range"
    # either PATH_ATTACK or PATH_CHAFF
    directory = os.fsencode(path)
    for host in IP_RANGE:
        for fil in os.listdir(directory):
            filename = os.fsdecode(fil)
            run = dicti[filename]
            run = run.replace(filename, path+'\\'+filename+' {}'.format(host))

            temp = run

            launch = utilities.create_child_gen(run)
            complete = False
            s = time.time()
            while not complete:
                complete = True
                if launch.poll() == 0:
                    response = str(launch.communicate())
                    # COMMENT OUT THIS LINE TO NOT SUBMIT THE FLAG
                    # BASED ON WHATEVER IS SENT TO STDOUT
                    # utilities.submit_flag(SUBMIT_FLAG_IP, SUBMIT_FLAG_PORT,
                    #                       response)
                    point = sub.submit(SUBMIT_FLAG_IP,response.strip())
                    # TODO make sure this is correct
                    with open(log, 'a') as logpointer:
                        logpointer.write('%s success: %s %s\n' % (str(
                                         filename), response, point))
                    # remove.append(launch)
                    # push to logfile success
                elif launch.poll()== None:
                    e = time.time()
                    if int(e-s) > 5:
                        print(filename+' on going')
                        s=time.time()
                    complete = False
                else:
                    if launch.poll()==0:
                        response = str(launch.communicate())
                        with open(log, 'a') as logpointer:
                            logpointer.write(filename
                                         +' success: '+response+'\n')
                    else:
                        print('it still failed')
        print(host,'is Complete. Moving to next...')
    return "{} is Done".format(path)


def main(cwd):
    # checks for the type
    attack_dictionary = {}
    chaff_dictionary = {}
    # Either preferences in main or here
    # read_preferences()
    # which, dicti, path
    #run_processes("Chaff", chaff_dictionary, PATH_CHAFF, "chaff.log")
    print(run_processes("Attacks", attack_dictionary,cwd, "attack.log"))

def func(cwd):
    parent = threading.Thread(target=main,args=(cwd,))
    parent.start()
data=[]
for dir in os.listdir(PATH_ATTACK):
    data.append(PATH_ATTACK+'\\'+dir)

for dir in data:
    func(dir)
