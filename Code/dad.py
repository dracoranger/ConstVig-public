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

class CHILD:
    #Summary of behavior: tracks each child and information pertinent to the child
    #Public methods: get_listener, get_socket, get_port, set_port, get_name, num_deaths, inc_deaths, reset_deaths, get_deaths, is_alive, is_keep_running, update_is_alive, toggle_keep_running, recreate_subprocess
    #Instance variables: None
    #Creator: Tate Bowers
    def __init__(self, nam):
        self.name = nam
        self.alive = False
        self.keep_running = True
        self.deaths = 0
        #Spawn process with cmd console(?)
        self.process = utilities.create_child_gen("python "+ self.name +".py")

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
    #Summary of behavior: starts, restarts, and manages the child processes
    #Arguments: None
    #Return values:
    #Side effects: child processes launched and monitored for success
    #Exceptions raised:
    #Restrictions on when it can be called: None

    config = utilities.parse_config('dad')
    death_limit = int(config['death_limit'])
    round_length = int(config['round_length'])
    total_rounds = int(config['total_rounds'])
    time_between_check = int(config['time_between_check'])
    log_file = config['log_file']

    with open(log_file, 'a') as logpointer:
        logpointer.write("Began operations at "+str(time.time())+'\n')

    child = CHILD("ChildNO")

    for i in range(0, total_rounds):
        time_start = time.time()
        time_rec = time.time()
        while time.time() - time_start < round_length:
            print(str(time.time()-time_start))
            if utilities.check_input(child.process.poll(), 1):
                if child.process.poll() == 0:
                    response = str(child.process.communicate())
                    with open(log_file, 'a') as logpointer:
                        logpointer.write('%s success: %s at %s\n' % (
                                         child.get_name(), response, str(time.time())))
                else:
                    response = str(child.process.communicate())
                    with open(log_file, 'a') as logpointer:
                        logpointer.write('%s failure: %s at %s\n' % (
                                         child.get_name(), response, str(time.time())))
                    print(child.get_name()+response)
            elif isinstance(child.process.poll(), type(None)):
                with open(log_file, 'a') as logpointer:
                    logpointer.write('%s Ongoing at %s\n' % (
                                     child.get_name(), str(time.time())))
                #print(child.get_name()+' on going: possibly too many files being launched')
            else:
                print("please look up what happens if subprocess.poll() doesn't return 1 or None")
            time.sleep(time_between_check)
        if isinstance(child.process.poll(), type(None)):
            print(child.get_name()+' on going: possibly too many files being launched')
        child.recreate_subprocess()
        print("round "+str(i)+" complete")
    with open(log_file, 'a') as logpointer:
        logpointer.write('Ended operations at %s\n' % (
                     str(time.time())))
    print("fully complete")

#Runs the main function
print("starting "+str(time.time()))
main()
