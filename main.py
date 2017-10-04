'''
main.py
'''

#import statements
#Utilities function
#time
#easysockets?

#any global constants
PATH = ''#file path of function
SETTINGS = ''#name of function
DEATH_LIMIT = 5
ROUND_LENGTH = 30
ROUND_NUMBER = 0
TIME_BETWEEN_CHECK = 5

#structures
TARGET#
#targets, array of target?
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
    ROUND_LENGTH, ROUND_NUMBER, TARGETS, ADDITONAL = parse(PATH, SETTINGS)

    setSettings=settings(ADDITONAL)#changes the settings outside the major timing results and attacking method

    #generate children
    childMaster[5]
    childMaster[0]=childUI#user input allows for input at any time, rather than needing to wait
    childMaster[1]=childNI#Network IN, detects and stores network flows into system.  May want to integrate with wireshark
    childMaster[2]=childNO#Network OUT, launches attacks
    childMaster[3]=childParse#deals with updates to the settings file, new files put into attacks folder
    childHackArray[]# push down to network outgoing? Stores each hack, ensures that failing hack only kills itself, not everything.

    lastTime= time.time()

    for i in range(0, ROUND_NUMBER):
        #wait on user input, returns from NI or NO
        #push information to logging
        #if time is > TIME_BETWEEN_CHECK
            #iterate through childMaster, check that all are alive
            #if one is dead, try to restart
            #check how many times that child has died
                #if child is above limit, alert user and ask if push through anyway
            #write to error log (call error, which pushes it to child process)
            #Alert user if necessary
            #write last actions of children so can resume from that point ? is this necessary


    #round length is minutes? seconds? per round, and controls how often the NO runs, and how often NI detects
    #round number determines the number of rounds
    #Target num data structure that contains information on who to attack, who not to attack, expected operating systems, attacks to ignore, more data will be there.
'''
error catching function
TODO: can you even have an error catching function or is it try and catch

'''
def error():


'''
logging function:


'''
def log(inpu):
    if(!utlilites.check_input('str',inpu))
        #FAIL RETURN TO START!

'''
UI

'''
def ui():

'''

'''
