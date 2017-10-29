'''
main.py

Creator:
Input:
Output:
This function
'''

import time
import os
import subprocess
import utilities
#Utilities function
#easysockets?

#any global constants- there should be none
#might need log file location
LOG_FILE = 'log'
PATH = os.path.dirname(os.path.realpath(__file__))#file path of settings file
CHILD_NUM = 4

#structures
class TARGET: #target data, such as IP and type
    '''
    Creator: Tate Bowers
    Input: TODO
    Output: TODO
    This function takes in targeting formation and stores it for use later
    just an intention at the moment
    '''
    def __init__(self, placeholder):
        self.ip_addr = 0 #make attack vars, need to make integrate well with networking pieces
#targets, array of target?


class CHILD:
    '''
    Creator: Tate Bowers
    Input: self, name of the process that is to be run (needs to be the name of the file)
    Output: look at get and set functions
    This function creates a child structure
    Child class contains the data necessary to lookup and check the child
    Name is the name of the child process being run
        must be the same as the name of the file minus python
    alive is whether or not its being run TODO: Make that update properly
    keep_running is whether or not it will continue to be spawned if it dies
    deaths is the number of times that process has died
    process creates the Popen child process
    UPDATE 10-22: Changed from subprocesses to Popen, which is the thing subprocesses is built on

    '''
    def __init__(self, nam):
        self.name = nam
        self.alive = False
        self.keep_running = True
        self.deaths = 0
        self.process = utilities.create_child(self.name, '')

    def get_name(self):
        '''
        self explanatory
        '''
        return self.name

    def num_deaths(self):
        '''
        self explanatory
        '''
        return self.deaths

    def inc_deaths(self):
        '''
        self explanatory
        '''
        self.deaths = self.deaths + 1

    def reset_deaths(self):
        '''
        self explanatory
        '''
        self.deaths = 0

    def get_deaths(self):
        '''
        returns number of times child has died
        '''
        return self.deaths

    def is_alive(self):
        '''
        self explanatory
        '''
        return self.alive

    def is_keep_running(self):
        '''
        returns whether the child is to restart if it dies
        '''
        return self.keep_running

    def update_is_alive(self, boo):
        '''
        self explanatory
        '''
        self.alive = boo


    def toggle_keep_running(self):
        '''
        switches the state of whether the child restarts upon death
        '''
        if self.keep_running:
            self.keep_running = False
        else:
            self.keep_running = True

    def recreate_subprocess(self):
        '''
        kills and then creates the child process
        '''
        self.process.kill()
        self.process = utilities.create_child(self.name, '')

def main():
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
    settings = '' #other settings stuff, placeholder currently
    death_limit = 5
    round_length = [300, 300, 300, 300, 300]#array of round lengths
    round_number = 0
    safety_buffer = 10
    time_between_check = 5
    global LOG_FILE
    global SETTING

    settings = [PATH, settings, death_limit, round_length,
                round_number, time_between_check, LOG_FILE]

    round_length, round_number, targets, additional = parse_settings(PATH,
                                                                     settings)
    #additional is a temp name here

    #setSettings = parse_settings(additional)
    #changes the settings outside the major timing results and attacking method

    if LOG_FILE == "":
        LOG_FILE = set_log_file(PATH)
        success = log('Began operations at '+str(time.time()))
        if success != 1:
            print("log failure")

    #childmaster = [CHILD('ChildFS')]
    #childmaster.append(CHILD('ChildNI'))
    #childmaster.append(CHILD('ChildNO'))
    #childmaster.append(CHILD('ChildUI'))
    childmaster = [CHILD('ChildNI')]

    #childHackArray=[0]
    # push down to network outgoing? Stores each hack,
    # ensures that failing hack only kills itself, not everything.


    for i in range(0, round_number):
        time_start = time.time()
        time_rec = time.time()
        while time.time() - time_start < round_length[i] + safety_buffer:

            #wait on user input, returns from NI or NO
            #push information to logging
            #Todo make it so that if child is alive, actually make child.is_alive true
            #print(str(time.time()-time_start))
            if time.time()-time_rec >= time_between_check:
                print(str(time.time()-time_start))
                for child in childmaster:
                    print(child.get_name()+' '+str(child.process.poll()))
                    #if child.process.poll() == None:
                    if isinstance(child.process.poll(), type(None)):
                        child.update_is_alive(True)
                    #need to figure out how to replace with necessary data
                #for num in range (0, CHILD_NUM):
                    #if childmaster[num].:
                    if child.is_alive():
                        #temp = child.get_name() + ' is alive!'
                        #print(temp)
                        inpu = get_input()
                        outpu = child.process.communicate(bytes(inpu,'ascii'))#should communicate with the process
                        print(outpu)
                        #Todo make outpu useful
                    elif child.is_keep_running():
                        child.recreate_subprocess()
                        child.inc_deaths()
                        temp = child.get_name()+''' has died.
                        Total deaths for '''+ child.get_name()+": "+str(child.get_deaths())
                        log(temp)
                        if child.get_deaths() > death_limit:
                            temp = child.get_name()+''' has
                             died '''+ str(child.get_deaths()) +" times. Continue anyways (y/n)?"
                            cont = input(temp)
                            print(cont)
                            if cont[:1].upper() == "N":
                                child.toggle_keep_running()
                time_rec = time.time()
                        #Alert user if necessary
                        #write last actions of children so can resume from that point ?

        print('round '+str(i)+' complete')
    print('fully complete')

    #round length is minutes? seconds? per round,
    # and controls how often the NO runs, and how often NI detects
    #round number determines the number of rounds
    #Target num data structure that contains information on who to attack,
    # who not to attack, expected operating systems, attacks to ignore, more data will be there.

def log(inpu):
    '''
    Creator: Tate Bowers
    Input: string that should be pushed to the logging file
    Output: updated logging file, nothing returned to user
    This function pushes strings to the logging file for future observation
    appends it to the end of the file

    '''
    ret = -1
    if utilities.check_input('str', inpu):
        temp = open(PATH+'\\'+LOG_FILE, "r+")#should take care of the LOG_FILE not being created
        temp.write(inpu+'\n')
        temp.close()
        #FAIL RETURN TO START!
        ret = 1
    return ret

def gui_minus():
    '''
    Creator: Tate Bowers
    Input: none
    Output: none
    This function acts as the debugging function while the actual user
     input child is being generated
    '''
    return ''

def set_log_file(path):
    '''
    Creator: Tate Bowers
    Input: intended file location
    Output: returns the file name
    This function creates and returns the log file
    the log file is named log+the day+ the hour+ the minute to prevent overlaps
    '''
    ret = -1
    if utilities.check_input('str', path):
        nam = 'log'+ time.strftime('%d_%h_%m')
        ret = nam
    temp = open(path+nam, 'w+')
    temp.close()
    return ret


def parse_settings(path, name):
    '''
    Creator: Tate Bowers
    Input: path of settings file, name of settings file
    Output: returns settings as an array
    This function parses the settings file, returns it as array
    TODO: properly parse settings file, need to talk with group to go over it
    '''
    current_setting = ''
    placeholder = ''
    make_happy = 0
    ret = [[40, 40, 40, 40, 40], 5, '', '']
    if utilities.check_input('str', path):
        if utilities.check_input('str', name):
            fil = open(path+name, 'r')
            for i in fil.read():
                if current_setting == '':
                    current_setting = i[:-1]
                elif current_setting == placeholder:
                    #do stuff
                    make_happy = make_happy + 1
                elif current_setting == placeholder:
                    #do stuff
                    make_happy = make_happy + 1
                else:
                    log('Unknown Setting')

    return ret[0], ret[1], ret[2], ret[3]


def get_input():
    '''
    Creator: Tate Bowers
    Input: unknown
    Output: unknown
    This function will be filled out later
    gets data from the command buffer ?
    TODO: fill out logic
    '''
    #list of queues?
    return 'Is this what is causing the failue?'


#Runs the main function
print('starting '+str(time.time()))
main()
