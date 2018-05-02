# handles traffic leaving to the rest of the network
'''
 NAME: Child Network Out
 FILE: ConstVig/Code/childNO.py
 CLASSES: N/A
 EXCEPTIONS:
 FUNCTIONS:
   main
   iter_thru_config
   run_processes
'''
import os
import time
import ipaddress
import random
import utilities
import ssResponse


# Constants & user set variables (naming exception made for variables)
dictionA = utilities.parse_config('Attacks')
dictionC = utilities.parse_config('Chaff')
dictionNO = utilities.parse_config('NetworkOut')
dictionLaunch = utilities.parse_config('dad')
PATH_ATTACK = dictionNO['path_attack']
PATH_CHAFF = dictionNO['path_chaff']
PORTS = dictionNO['ports'].split(',')
SUBMIT_FLAG_PORT = dictionNO['submit_flag_port']
SUBMIT_FLAG_IP = dictionNO['submit_flag_ip']
RANDOMIZED_AND_SPACED = int(dictionNO['randomized_and_spaced'])
CHAFF_PER_ATTACK = int(dictionNO['chaff_per_attack'])
ROUND_LENGTH = int(dictionLaunch['round_length'])
SAFETY_BUFFER = int(dictionNO['safety_buffer'])
SUBMIT_AUTOMATICALLY = int(dictionNO['submit_flags_automatically'])
if int(dictionNO['use_ip_range']):
    IP_RANGE = list(ipaddress.ip_network(dictionNO['ip_range']).hosts())
else:
    IP_RANGE = dictionNO['ip_list'].split(',')

def iter_thru_config(which, dicti):
    # "which" is either "Attack" or "Chaff"
    diction = utilities.parse_config(which)
    for i in diction:
        if not i in dicti:
            # dicti is either chaff or attack dictionary
            dicti[i] = diction[i]

def generate_process_names(which, dicti, path):
    # "which" is either "Attack" or "Chaff"
    iter_thru_config(which, dicti)
    # either PATH_ATTACK or PATH_CHAFF
    directory = os.fsencode(path)
    process_names = []
    for fil in os.listdir(directory):
        filename = os.fsdecode(fil)
        run = dicti[filename]
        run = run.replace(filename, path+'\\'+filename)
        if '-f' in run:
            run = run.replace('-f', '-f '+SUBMIT_FLAG_IP+','
                              +SUBMIT_FLAG_PORT)
        temp = run
        if '-ip' in temp and '-p' in temp:
            for p in PORTS:
                for i in IP_RANGE:
                    temp = run.replace('-ip', '-ip '+str(i))
                    temp = temp.replace('-p', '-p '+str(p))
                    process_names.append((temp, filename))
        elif '-ip' in temp:
            for i in IP_RANGE:
                temp = run.replace('-ip', ''+str(i))
                process_names.append((temp, filename))
        elif '-p' in temp:
            for p in PORTS:
                temp = run.replace('-p', '-p '+str(p))
                process_names.append((temp, filename))
        else:
            process_names.append((temp, filename))
    return process_names

#TODO Attack in series for a single service
#TODO Attack in parallel for every service
#Simply runs given processes
def run_processes(attacks, log_file):
    launch_storage = []
    launch_order = []
    time_between_launches = int((ROUND_LENGTH-SAFETY_BUFFER)/(len(attacks)))
    for attack, filename in attacks:
        launch = utilities.create_child_gen(attack)
        launch_storage.append(launch)
        launch_order.append(filename)
        time.sleep(time_between_launches)
    utilities.log_data(log_file, 'All attacks launched\n')
    complete = False
    while not complete:
        remove = []
        curr_num = 0
        time.sleep(3)
        complete = True
        for launch in launch_storage:
            if utilities.check_input(launch.poll(), 1):
                if launch.poll() == 0:
                    response = str(launch.communicate())
                    if SUBMIT_AUTOMATICALLY:
                        #reply = utilities.submit_flag(SUBMIT_FLAG_IP, SUBMIT_FLAG_PORT,
                        #                              response[1])
                        reply = ssResponse.submit(SUBMIT_FLAG_IP,str(response))
                        utilities.log_data(log_file, 'Reply from server: ' + str(reply)+'\n')
                    utilities.log_data(log_file, '%s success: %s\n' %
                                       (str(launch_order[curr_num]), response))
                    remove.append(launch)
                else:
                    response = str(launch.communicate())
                    utilities.log_data(log_file, '%s failure: %s\n' %
                                       (str(launch_order[curr_num]), response))
                    print(str(launch_order[curr_num])+response)
                    remove.append(launch)
            elif isinstance(launch.poll(), type(None)):
                utilities.log_data(log_file, '%s ongoing: %s\n' %
                                   (str(launch_order[curr_num]), response))
                print(launch_order[curr_num]+' on going')
                complete = False
            curr_num = curr_num + 1
        for i in remove:
            temp = launch_storage.index(i)
            launch_storage.remove(i)
            launch_order.pop(temp)

#Generates process names and launches processes
#not feasible for randomized and spaced attacks
def generate_and_run_processes(which, dicti, path, log_file):
    # "which" is either "Attack" or "Chaff"
    iter_thru_config(which, dicti)
    # either PATH_ATTACK or PATH_CHAFF
    directory = os.fsencode(path)
    launchStorage = []
    launchOrder = []
    for fil in os.listdir(directory):
        filename = os.fsdecode(fil)
        run = dicti[filename]
        run = run.replace(filename, PATH_ATTACK+'\\'+filename)
        if '-f' in run:
            run = run.replace('-f', '-f '+SUBMIT_FLAG_IP+','
                              +SUBMIT_FLAG_PORT)
        temp = run
        if '-ip' in temp and '-p' in temp:
            for p in PORTS:
                for i in IP_RANGE:
                    temp = run.replace('-ip', '-ip '+str(i))
                    temp = temp.replace('-p', '-p '+str(p))
                    launch = utilities.create_child_gen(temp)
                    launchStorage.append(launch)
                    launchOrder.append(filename)
        elif '-ip' in temp:
            for i in IP_RANGE:
                temp = run.replace('-ip', '-ip '+str(i))
                launch = utilities.create_child_gen(temp)
                launchStorage.append(launch)
                launchOrder.append(filename)
        elif '-p' in temp:
            for p in PORTS:
                temp = run.replace('-p', '-p '+str(p))
                launch = utilities.create_child_gen(temp)
                launchStorage.append(launch)
                launchOrder.append(filename)
        else:
            launch = utilities.create_child_gen(run)
            launchStorage.append(launch)
            launchOrder.append(filename)
    complete = False
    while not complete:
        remove = []
        curr_num = 0
        time.sleep(3)
        complete = True
        for launch in launchStorage:
            if utilities.check_input(launch.poll(), 1):
                if launch.poll() == 0:
                    response = str(launch.communicate())
                    if SUBMIT_AUTOMATICALLY:
                        reply = utilities.submit_flag(SUBMIT_FLAG_IP, SUBMIT_FLAG_PORT,
                                                      response)
                        utilities.log_data(log_file, 'Reply from server: ' + reply)
                    utilities.log_data(log_file, '%s success: %s\n' %
                                       (str(launchOrder[curr_num]), response))
                    remove.append(launch)
                else:
                    response = str(launch.communicate())
                    utilities.log_data(log_file, '%s failure: %s\n' %
                                       (str(launchOrder[curr_num]), response))
                    print(str(launchOrder[curr_num])+response)
                    remove.append(launch)
            elif isinstance(launch.poll(), type(None)):
                utilities.log_data(log_file, '%s ongoing: %s\n' %
                                   (str(launchOrder[curr_num]), response))
                print(launchOrder[curr_num]+' on going')
                complete = False
            curr_num = curr_num + 1
        for i in remove:
            temp = launchStorage.index(i)
            launchStorage.remove(i)
            launchOrder.pop(temp)


def main():
    attack_dictionary = {
    }
    chaff_dictionary = {
    }

    if RANDOMIZED_AND_SPACED == 1:
        processes = generate_process_names('Attacks', attack_dictionary, PATH_ATTACK)
        for i in range(CHAFF_PER_ATTACK):
            processes = processes + generate_process_names('Chaff', chaff_dictionary, PATH_CHAFF)
        random.shuffle(processes)
        run_processes(processes, 'mixed.log')
    else:
        generate_and_run_processes('Chaff', chaff_dictionary, PATH_CHAFF, 'chaff.log')
        generate_and_run_processes('Attacks', attack_dictionary, PATH_ATTACK, 'attack.log')

main()
