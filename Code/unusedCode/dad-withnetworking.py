import time
import os
import socket
import threading
import utilities

#import subprocess
#Utilities function
#easysockets?
#twisted.internet?

#runs and manages everything, including child processes

#Classes:
#TARGET -- will hold target IP addresses. To be finished later.
#CHILD -- each child is a processes, e.g. NetIn (NI) that serves a specific purpose.
#Exceptions:
#Functions:
#main -- loops through the children, checking for deaths and restarting when appropriate
#log -- adds to the log file to track errors, etc.
#gui_minus -- acts as a debugger
#set_log_file -- creates and returns the log file
#parse_settings -- parses the settings file, returning as a array
#get_input -- gets input from the user interface

#structures

class chatThread(threading.Thread):
    #Class: chatThread
    #Purpose: Each client connection spawns a new chatThread object
    #and interaction with the client is via this thread.

    def __init__(self, parent, csock):
        #chatThread constructor
        # Call parent class constructor
        threading.Thread.__init__(self)
        self.csock = csock

        # Need to be able to reference parent to send messages to all threads
        self.parent = parent

    def run(self):
        #Main loop for chatThread objects

        try:
            while 1:
                # Receive chat message from client
                message = self.csock.recv(1024)
                message = message.decode()
                print(message)
                # reading from a closed socket will yield empty messages (0 bytes)
                if len(message) == 0:
                    raise Exception("Client closed unexpectedly")

                # Call method in parent that iterates through all
                # connected client threads and sends message to all


                #self.parent.sendToAll(message.encode())

        except:  # handle exception type
            # client has left, close socket and end thread
            self.csock.close()

    def sendMsg(self, msg):
        #Send a message to the client in this thread.
        # message must be in bytes format
        self.csock.send(msg)

class CHILD:

    #each unit of functionality in the program is given to a child process.

    #Summary of behavior: tracks each child and information pertinent to the child
    #Public methods: get_listener, get_socket, get_port, set_port, get_name, num_deaths, inc_deaths, reset_deaths, get_deaths, is_alive, is_keep_running, update_is_alive, toggle_keep_running, recreate_subprocess
    #Instance variables: None
    #Creator: Tate Bowers

    #UPDATE 10-22: Changed from subprocesses to Popen, which is the thing subprocesses is built on
    #TODO: Kill socket when dying

    def __init__(self, nam, por):
        #class constructor documentation goes here
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", por))
        sock.listen(5)
        self.name = nam
        self.alive = False
        self.keep_running = True
        self.deaths = 0
        self.process = utilities.create_child_gen("python "+ self.name +".py")
        self.port = por
        self.listener = ""
        self.socket = sock#utilities.comm_in(self.port-100)

        #need to catch socket errors
    def set_listener(self, inp):
        #self explanatory
        self.listener = inp

    def get_listener(self):
        #self explanatory
        return self.listener

    def get_socket(self):
        #self explanatory
        return self.socket

    def set_socket(self, inp):
        #self explanatory
        self.socket = inp

    def get_port(self):
        #self explanatory
        return self.port

    def set_port(self, new_port):
        #self explanatory
        self.port = new_port

    def get_name(self):
        #self explanatory
        return self.name

    def num_deaths(self):
        #self explanatory
        return self.deaths

    def inc_deaths(self):
        #self explanatory
        self.deaths = self.deaths + 1

    def reset_deaths(self):
        #self explanatory
        self.deaths = 0

    def get_deaths(self):
        #returns number of times child has died
        return self.deaths

    def is_alive(self):
        #self explanatory, returns Boolean
        return self.alive

    def is_keep_running(self):
        #returns whether the child is to restart if it dies
        return self.keep_running

    def update_is_alive(self, boo):
        #self explanatory
        self.alive = boo

    def toggle_keep_running(self):
        #switches the state of whether the child restarts upon death
        if self.keep_running:
            self.keep_running = False
        else:
            self.keep_running = True

    def recreate_subprocess(self):
        #kills and then creates the child process
        self.process.kill()
        self.process = utilities.create_child_gen("python "+ self.name +".py")

def main():
    #checks on, spawns, and recreates child processes

    #Summary of behavior: starts, restarts, and manages the child processes
    #Arguments: None
    #Return values:
    #Side effects: child processes launched and monitored for success
    #Exceptions raised:
    #Restrictions on when it can be called: None

    #main function

    #Basic loop
    #0. read in settings data
    #1. Spin up children
    #    a. log errors
    #    b. restart if failure
    #    c. prompt if multiple failures
    #2. children for
    #    a. UI
    #    b. Network incoming
    #    c. Network outgoing
    #    d. filesystem parsing
    #    e. spin up individual child for each hack discovered by filesystem
    #3. iterate through rounds
    #4. every x seconds, check to see that children are still alive
    #5. attempt to restore any dead children, prompting user
    #6. write out error log
    #7. generate alerts
    #8. save the state of the children in case of failure -- is this necessary?

    #Conditionals
    #if reach end of the rounds, prompt for do more
    #if children crash, prompt user to restart, log, prompt if multiple failures on same child

    #possibles
    #sync timer?  Probably not necessary on same system
    config = utilities.parse_config('dad')
    death_limit = int(config['death_limit'])
    round_length = [300, 300, 300, 300, 300]#array of round lengths
    total_rounds = int(config['total_rounds'])
    safety_buffer = int(config['safety_buffer'])
    time_between_check = int(config['time_between_check'])
    log_file = config['log_file']


    #additional is a temp name here

    #setSettings = parse_settings(additional)
    #changes the settings outside the major timing results and attacking method

    if LOG_FILE == "":
        LOG_FILE = set_log_file(PATH)
        success = log("Began operations at "+str(time.time()))
        if success != 1:
            print("log failure")

    childmaster = [CHILD("ChildUI",15550)]
    #childmaster.append(CHILD("ChildNI",15551))
    #childmaster.append(CHILD("ChildNO",15552))
    childmaster.append(CHILD("ChildDeath",15551))
    #childmaster = [CHILD("ChildNO", 15551)]
    time.sleep(1)
    #generate sockets
    for i in childmaster:
        connection_socket, addr = i.get_socket().accept()
        i.set_listener(chatThread(i.get_port(), connection_socket))
        # Add new chatThread to list of all threads
        i.set_socket(connection_socket)
        #start new chatThread
        i.get_listener().start()
        print(i.get_listener())
        #should generate the proper connection and acception
    #childHackArray=[0]
    # push down to network outgoing? Stores each hack,
    # ensures that failing hack only kills itself, not everything.


    for i in range(0, total_rounds):
        time_start = time.time()
        time_rec = time.time()
        #start automated launcher?
        while time.time() - time_start < round_length[i] + safety_buffer:
            #TODO Implement properly
            #if not i.get_listener().isAlive():
            #    i.get_listener().join()
            #    i.set_listener('')
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
                    if isinstance(child.process.poll(), type(0)):
                        child.update_is_alive(False)
                    print(child.is_alive())
                    if child.is_alive():
                        child.get_socket().send(get_input().encode())
                    elif child.is_keep_running():
                        #child.recreate_subprocess()
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
    for child in childmaster:
        child.get_listener().join()
        child.set_listener('')
        child.get_socket().close()
        child.process.kill()
        print(child.get_name()+" "+str(child.process.poll()))
    #    child.get_listener().join()




    #round length is minutes? seconds? per round,
    # and controls how often the NO runs, and how often NI detects
    #round number determines the number of rounds
    #Target num data structure that contains information on who to attack,
    # who not to attack, expected operating systems, attacks to ignore, more data will be there.

def log(inpu):
    #Creator: Tate Bowers
    #Input: string that should be pushed to the logging file
    #Output: updated logging file, nothing returned to user
    #This function pushes strings to the logging file for future observation
    #appends it to the end of the file

    ret = -1
    if utilities.check_input("str", inpu):
        temp = open(PATH+"\\"+LOG_FILE, "r+")#should take care of the LOG_FILE not being created
        temp.write(inpu+"\n")
        temp.close()
        #FAIL RETURN TO START!
        ret = 1
    return ret


def parse_settings(path, name):
    #TODO -- fill in one line Summary

    #Summary of behavior: This function parses the settings file, returns it as array
    #Arguments: path of settings file, name of settings file
    #Return values:settings as an array
    #Side effects:
    #Exceptions raised:
    #Restrictions on when it can be called: None
    return "Incomplete"

def get_input():
    #Creator: Tate Bowers
    #list of queues?
    return "Incomplete"


#Runs the main function
print("starting "+str(time.time()))
main()