import time
import os
import socket
import threading
import utilities

#import subprocess
#Utilities function
#easysockets?
#twisted.internet?

""" runs and manages everything, including child processes

Classes:
TARGET -- will hold target IP addresses. To be finished later.
CHILD -- each child is a processes, e.g. NetIn (NI) that serves a specific purpose.
Exceptions:
Functions:
main -- loops through the children, checking for deaths and restarting when appropriate
log -- adds to the log file to track errors, etc.
gui_minus -- acts as a debugger
set_log_file -- creates and returns the log file
parse_settings -- parses the settings file, returning as a array
get_input -- gets input from the user interface
"""




#any global constants- there should be none
#might need log file location
LOG_FILE = "log"
PATH = os.path.dirname(os.path.realpath(__file__))#file path of settings file
CHILD_NUM = 4

#structures
class TARGET:
    """ tracks target data, such as IP and type

    Summary of behavior: This function takes in targeting formation and stores it for use later
    just an intention at the moment
    Public methods:
    Instance variables: None
    Creator: Tate Bowers
    """
    def __init__(self, placeholder):
        """class constructor documentation goes here"""
        self.ip_addr = 0 #make attack vars, need to make integrate well with networking pieces
    #targets, array of target?



class CHILD:

    """ each unit of functionality in the program is given to a child process.

    Summary of behavior: tracks each child and information pertinent to the child
    Public methods: get_listener, get_socket, get_port, set_port, get_name, num_deaths, inc_deaths, reset_deaths, get_deaths, is_alive, is_keep_running, update_is_alive, toggle_keep_running, recreate_subprocess
    Instance variables: None
    Creator: Tate Bowers

    UPDATE 10-22: Changed from subprocesses to Popen, which is the thing subprocesses is built on
    TODO: Kill socket when dying
    """
    def __init__(self, nam, por):
        """class constructor documentation goes here"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", por))
        sock.listen(5)
        self.name = nam
        self.alive = False
        self.keep_running = True
        self.deaths = 0
        self.process = utilities.create_child(self.name, "")
        self.port = por
        self.listener = ""
        self.socket = sock#utilities.comm_in(self.port-100)
        self.connect_to_child = sock

        #might need to catch socket errors
    def engage_listener(self):
        self.listener=threading.Thread(target=utilities.readFromServer(), args=([self.connect_to_child]))

    def get_child_connection(self):
        """returns the socket that is attached to the child process"""
        return self.connect_to_child

    def get_listener(self):
        """self explanatory"""
        return self.listener

    def get_socket(self):
        """self explanatory"""
        return self.socket

    def get_port(self):
        """self explanatory"""
        return self.port

    def set_port(self, new_port):
        """self explanatory"""
        self.port = new_port

    def get_name(self):
        """self explanatory"""
        return self.name

    def num_deaths(self):
        """self explanatory"""
        return self.deaths

    def inc_deaths(self):
        """self explanatory"""
        self.deaths = self.deaths + 1

    def reset_deaths(self):
        """self explanatory"""
        self.deaths = 0

    def get_deaths(self):
        """returns number of times child has died"""
        return self.deaths

    def is_alive(self):
        """self explanatory"""
        return self.alive

    def is_keep_running(self):
        """returns whether the child is to restart if it dies"""
        return self.keep_running

    def update_is_alive(self, boo):
        """self explanatory"""
        self.alive = boo

    def toggle_keep_running(self):
        """switches the state of whether the child restarts upon death"""
        if self.keep_running:
            self.keep_running = False
        else:
            self.keep_running = True

    def recreate_subprocess(self):
        """kills and then creates the child process"""
        self.process.kill()
        self.process = utilities.create_child(self.name, "")

def main():
    """ checks on, spawns, and recreates child processes

    Summary of behavior: starts, restarts, and manages the child processes
    Arguments: None
    Return values:
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called: None

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

    """
    settings = "" #other settings stuff, placeholder currently
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
        success = log("Began operations at "+str(time.time()))
        if success != 1:
            print("log failure")

    #childmaster = [CHILD("ChildFS",15550)]
    #childmaster.append(CHILD("ChildNI",15551))
    #childmaster.append(CHILD("ChildNO",15552))
    #childmaster.append(CHILD("ChildUI",15553))
    childmaster = [CHILD("ChildNI", 15551)]
    time.sleep(1)
    #generate sockets

    threads_holder = []
    for i in childmaster:
        i.get_socket().accept()
        i.engage_listener()
        i.get_listener().start()
        #threads_holder.append(i.get_listener())
        #\/ is equiv to ^
        #chatter = chatThread(self, i.get_socket)
        #i.set_child_connection()
        """
        should generate the proper connection and acception
        """
        #connectionSocket, addr = serverSocket.accept()
        #chatter = chatThread(self, connectionSocket)

        # Add new chatThread to list of all threads
        #self.mythreads.append(chatter)

        #start new chatThread
        #i.get_listener().start()
#                print("New client joined")

        #for thread in self.mythreads:
        #    if not thread.isAlive():
        #        thread.join()
        #        self.mythreads.remove(thread)
        #i.set_child_connection(i.get_port())
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
                    print(child.get_name()+" "+str(child.process.poll()))
                    #if child.process.poll() == None:
                    if isinstance(child.process.poll(), type(None)):
                        child.update_is_alive(True)
                    #need to figure out how to replace with necessary data
                #for num in range (0, CHILD_NUM):
                    #if childmaster[num].:
                    if child.is_alive():


                        child.get_socket().send(get_input().encode())
                        #temp = child.get_name() + " is alive!"
                        #print(temp)
                        #inpu = get_input()
                        #utilities.comm_out(get_input(), child.get_child_connection())
                        #output = child.get_socket().recv(1024).decode()
                        #outpu = child.process.communicate(bytes(inpu,"ascii"))
                        #should communicate with the process
                        #print(output) #should print automatically
        #https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
                        #Todo make outpu useful

                    elif child.is_keep_running():
                        child.recreate_subprocess()
                        child.inc_deaths()
                        temp = child.get_name()+""" has died.
                        Total deaths for """+ child.get_name()+": "+str(child.get_deaths())
                        log(temp)
                        if child.get_deaths() > death_limit:
                            temp = child.get_name()+""" has
                             died """+ str(child.get_deaths()) +" times. Continue anyways (y/n)?"
                            cont = input(temp)
                            print(cont)
                            if cont[:1].upper() == "N":
                                child.toggle_keep_running()
                time_rec = time.time()
                        #Alert user if necessary
                        #write last actions of children so can resume from that point ?

        print("round "+str(i)+" complete")
    print("fully complete")
    #    child.get_listener().join()
    for thread in threads_holder:
        thread.join()

    for child in childmaster:
        child.get_socket().close()

    #round length is minutes? seconds? per round,
    # and controls how often the NO runs, and how often NI detects
    #round number determines the number of rounds
    #Target num data structure that contains information on who to attack,
    # who not to attack, expected operating systems, attacks to ignore, more data will be there.

def log(inpu):
    """
    Creator: Tate Bowers
    Input: string that should be pushed to the logging file
    Output: updated logging file, nothing returned to user
    This function pushes strings to the logging file for future observation
    appends it to the end of the file

    """

    ret = -1
    if utilities.check_input("str", inpu):
        temp = open(PATH+"\\"+LOG_FILE, "r+")#should take care of the LOG_FILE not being created
        temp.write(inpu+"\n")
        temp.close()
        #FAIL RETURN TO START!
        ret = 1
    return ret

def gui_minus():
    """ TODO -- fill in one line Summary

    Summary of behavior: This function acts as the debugging function while the actual user
     input child is being generated
    Arguments: None
    Return values: None
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called: None
    Creator: Tate Bowers
    """
    return ""


def set_log_file(path):
    """
    Creator: Tate Bowers
    Input: intended file location
    Output: returns the file name
    This function creates and returns the log file
    the log file is named log+the day+ the hour+ the minute to prevent overlaps
    """
    ret = -1
    if utilities.check_input("str", path):
        nam = "log"+ time.strftime("%d_%h_%m")
        ret = nam
    temp = open(path+nam, "w+")
    temp.close()
    return ret


def parse_settings(path, name):
    """
    TODO -- fill in one line Summary

    Summary of behavior: This function parses the settings file, returns it as array
    Arguments: path of settings file, name of settings file
    Return values:settings as an array
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called: None
    """

    current_setting = ""
    placeholder = ""
    make_happy = 0
    ret = [[40, 40, 40, 40, 40], 5, "", ""]
    if utilities.check_input("str", path):
        if utilities.check_input("str", name):
            fil = open(path+name, "r")
            for i in fil.read():
                if current_setting == "":
                    current_setting = i[:-1]
                elif current_setting == placeholder:
                    #do stuff
                    make_happy = make_happy + 1
                elif current_setting == placeholder:
                    #do stuff
                    make_happy = make_happy + 1
                else:
                    log("Unknown Setting")

    return ret[0], ret[1], ret[2], ret[3]


def get_input():
    """
    Creator: Tate Bowers

    TODO: fill out logic
    """
    #list of queues?
    return "Is this what is causing the failue?"


#Runs the main function
print("starting "+str(time.time()))
main()
