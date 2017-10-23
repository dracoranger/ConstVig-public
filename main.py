'''
main.py
'''

#import statements
#Utilities function
#time
#easysockets?
import time
import timeit
import os
import subprocess
import utilities


#any global constants- there should be none
#might need log file location
LOG_FILE = 'log'
PATH = os.path.dirname(os.path.realpath(__file__))#file path of settings file
CHILD_NUM = 4

#structures
class TARGET: #target data, such as IP and type
    def __init__(self, PLACEHOLDER):
        self.ip = 0 #make attack vars, need to make integrate well with networking pieces
#targets, array of target?

'''
Child class contains the data necessary to lookup and check the child
Name is the name of the child process being run, must be the same as the name of the file minus python
alive is whether or not its being run TODO: Make that update properly
keep_running is whether or not it will continue to be spawned if it dies
deaths is the number of times that process has died
process creates the Popen child process UPDATE 10-22: Changed from subprocesses to Popen, which is the thing its built on

'''
class CHILD:
    def __init__(self, nam):
        self.name = nam
        self.alive = False
        self.keep_running = True
        self.deaths = 0
        self.process = utilities.create_child(self.name, '')

    def get_name(self):
        return self.name

    def num_deaths(self):
        return self.deaths

    def inc_deaths(self):
        self.deaths = self.deaths + 1

    def reset_deaths(self):
        self.deaths = 0

    def get_deaths(self):
        return self.deaths

    def is_alive(self):
        return self.alive

    def is_keep_running(self):
        return self.keep_running

    def update_is_alive(self, bytesFromProcessExitCode):
        if bytesFromProcessExitCode: #TODO make this functional
            self.alive = False
        else:
            self.alive = True

    def toggle_keep_running(self):
        if self.keep_running:
            self.keep_running = False
        else:
            self.keep_running = True

'''
main function

Basic loop
0. read in settings data
1. Spin up children
    a. log errors
    b. restart if failure
    c. prompt if multiple failures
2. children for
    a. UI
    b. Network incoming
    c. Network outgoing
    d. filesystem parsing
    e. spin up individual child for each hack discovered by filesystem
3. iterate through rounds
4. every x seonds, check to see that children are still alive
5. attempt to restore any dead children, prompting user
6. write out error log
7. generate alerts
8. save the state of the children in case of failure ? is this necessary

Conditionals
if reach end of the rounds, prompt for do more
if children crash, prompt user to restart, log, prompt if multiple failures on same child

possibles
sync timer?  Probably not necessary on same system

'''
def main():

    SETTING = ''#name of settings file
    SETTINGS = '' #other settings stuff, placeholder currently
    LOG_FILE = '' #log file name
    DEATH_LIMIT = 5
    ROUND_LENGTH = [300,300,300,300,300]#array of round lengths
    ROUND_NUMBER = 0
    SAFETY_BUFFER = 30
    TIME_BETWEEN_CHECK = 5
    #Unnessary because of struct addition
    #child_num_deaths[CHILD_NUM]
    #for i in range(0, CHILD_NUM):
    #    child_num_deaths.append(0)
    #    run_child.append(True)

    #is dealt with in log()
    #logBuffer = ''
    SETTINGS = [PATH, SETTINGS, DEATH_LIMIT, ROUND_LENGTH, ROUND_NUMBER, TIME_BETWEEN_CHECK, LOG_FILE]

    #ROUND_LENGTH, ROUND_NUMBER, TARGETS, ADDITONAL = parse_settings(PATH, SETTINGS)#additional is a temp name here

    #setSettings = parse_settings(ADDITONAL)#changes the settings outside the major timing results and attacking method

    if LOG_FILE == "":
        LOG_FILE = setLogFile(PATH)
        success = log('Began operations at '+str(time.time()))
        if success != 1:
            print("log failure")
    #generate children

    childMaster = [CHILD('childFS'), CHILD('childNI')]
    childMaster.append(CHILD('childNO'))
    childMaster.append(CHILD('childUI'))

    #childHackArray=[0]# push down to network outgoing? Stores each hack, ensures that failing hack only kills itself, not everything.


    for i in range(0, ROUND_NUMBER):
        time_start = time.time()
        while time.time() - time_start < ROUND_LENGTH[i] + SAFETY_BUFFER:

            #wait on user input, returns from NI or NO
            #push information to logging
            #TODO make it so that if child is alive, actually make child.is_alive true
            if time.time()-time_start >= TIME_BETWEEN_CHECK:
                print(str(time.time()-time_start))
                for child in childMaster:
                    print(child.process.poll())
                    if child.process.poll():
                        child.update_is_alive(True)
                    outpu = ''
                    inpu = ''#need to figure out how to replace with necessary data
                #for num in range (0, CHILD_NUM):
                    #if childMaster[num].:
                    if child.is_alive():
                        inpu = get_input()
                        outpu = child.process.communicate(inpu)#should communicate with the process
                        print(outpu)
                        #TODO make outpu useful
                    elif child.is_keep_running():
                        child.inc_deaths()
                        temp = child.get_name()+" has died. Total deaths for "+ child.get_name()+": "+str(child.get_deaths())
                        log(temp)
                        if child.get_deaths() > DEATH_LIMIT:
                            temp = child.get_name()+" has died "+ str(child.get_deaths()) +" times. Continue anyways (y/n)?"
                            cont = input(temp)
                            print(cont)
                            if cont[:1].upper() == "N":
                                child.toggle_keep_running()

                            '''
                            childMaster[n]=subprocess.run(childn)
                            child_num_deaths[n]+=1
                            log("%s has died. Total deaths for %s: %d" + child.toString, child.toString, child_num_deaths[n])
                            #(call error, which pushes it to child process)
                        if(child_num_deaths[n] >= DEATH_LIMIT)
                            continue = input("%s has died %d times. Continue anyways (y/n)?", child.toString, child_num_deaths[n])
                            if continue == 'n' run_child[n] = False
                            '''
            time_start=time.time()
                        #Alert user if necessary
                        #write last actions of children so can resume from that point ? is this necessary

        print('round '+i+'complete')
    print('fully complete')

    #round length is minutes? seconds? per round, and controls how often the NO runs, and how often NI detects
    #round number determines the number of rounds
    #Target num data structure that contains information on who to attack, who not to attack, expected operating systems, attacks to ignore, more data will be there.
'''
logging function:
takes in input and LOG_FILE and appends inpu to the current logging file

'''
def log(inpu):
    ret = -1
    if utilities.check_input('str',inpu):
        temp = open(PATH+'\\'+LOG_FILE, "r+")#should take care of the LOG_FILE not being created
        temp.write(inpu+'\n')
        temp.close()
        #FAIL RETURN TO START!
        ret = 1
    return ret
'''
UI
Debugging function while the actual user input child is being generated
'''
def guiMinus():
    return ''
'''
Creates and returns the log file
'''
def setLogFile(path):
    ret = -1
    if utilities.check_input('str', path):
        nam = 'log'+ time.strftime('%d_%h_%m')
        ret = nam
    temp = open(path+nam, 'w+')
    temp.close()
    return ret

'''
parses the settings file, returns it as array
TODO: properly parse settings file, need to talk with group to go over it
'''
def parse_settings(path, name):
    current_setting = ''
    PLACEHOLDER = ''
    make_happy = 0
    ret = [[300,300,300,300,300], 5, '', '']
    if utilities.check_input('str', path):
        if utilities.check_input('str', name):
            fil = open(path+name, 'r')
            for i in fil.read():
                if current_setting == '':
                    current_setting = i[:-1]
                elif current_setting == PLACEHOLDER:
                    #do stuff
                    make_happy = make_happy + 1
                elif current_setting == PLACEHOLDER:
                    #do stuff
                    make_happy = make_happy + 1
                else:
                    log('Unknown Setting')

    return ret[0], ret[1], ret[2], ret[3]

'''
gets data from the command buffer
TODO: fill out logic
'''
def get_input():
    #list of queues?
    return ''

print('starting '+str(time.time()))
main()
