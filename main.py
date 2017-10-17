'''
main.py
'''

#import statements
#Utilities function
#time
#easysockets?

#any global constants- there should be none
#might need log file location
LOG_FILE = ''
PATH = ''#file path of settings file

#structures
class TARGET: #
    def __init__():
        self.ip= 0 #make attack vars, need to make integrate well with networking pieces
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

    SETTING = ''#name of settings file
    DEATH_LIMIT = 5
    ROUND_LENGTH = [300]#array of round lengths
    round_number = 0
    SAFETY_BUFFER = 30
    TIME_BETWEEN_CHECK = 5

    logBuffer = ''
    SETTINGS = [PATH, SETTINGS, DEATH_LIMIT, ROUND_LENGTH, round_number, TIME_BETWEEN_CHECK, LOG_FILE]

    ROUND_LENGTH, ROUND_NUMBER, TARGETS, ADDITONAL = parse_settings(PATH, SETTINGS)#additional is a temp name here

    setSettings=settings(ADDITONAL)#changes the settings outside the major timing results and attacking method

    if LOG_FILE == "":
        LOG_FILE = setLogFile(PATH)
        logBuffer='Began operations at '+str(time.time())
        success = log(LOG_FILE, logBuffer)
        if success != 1:
            print("log failure")
    #generate children
    childMaster[5]
    try:
        childMaster[0]=subprocess.run(childUI)#user input allows for input at any time, rather than needing to wait
                                              #send stdout to buffer, to write to log
    except ChildProcessError:
        #run debug process and try again later
    except:
        #something else went wrong, try to make better

    try:
        childMaster[1]=childNI#Network IN, detects and stores network flows into system.  May want to integrate with wireshark
    except ChildProcessError:
        #run debug process and try again later
    except:
        #something else went wrong, try to make better
    try:
        childMaster[2]=childNO#Network OUT, launches attacks
    except ChildProcessError:
        #run debug process and try again later
    except:
        #something else went wrong, try to make better

    try:
        childMaster[3]=childParse#deals with updates to the settings file, new files put into attacks folder
    except ChildProcessError:
        #run debug process and try again later
    except:
        #something else went wrong, try to make better

    childHackArray[]# push down to network outgoing? Stores each hack, ensures that failing hack only kills itself, not everything.


    for i in range(0, ROUND_NUMBER):
        timeStart = time.time()
        while(time.time() - timeStart < ROUND_LENGTH[i] + SAFETY_BUFFER):

            #wait on user input, returns from NI or NO
            #push information to logging
            if(time.time()-timStart >= TIME_BETWEEN_CHECK)
                for(child in CHILD_NUM)
                    if(child.isDead)
                        childMaster[n]=subprocess.run(childn)
                        child_num_deaths[n]+=1
                    if(child_num_deaths[n] >= DEATH_LIMIT)
                        #alert user and ask if push through anyway
                    #write to error log (call error, which pushes it to child process)
                    #Alert user if necessary
                    #write last actions of children so can resume from that point ? is this necessary


    #round length is minutes? seconds? per round, and controls how often the NO runs, and how often NI detects
    #round number determines the number of rounds
    #Target num data structure that contains information on who to attack, who not to attack, expected operating systems, attacks to ignore, more data will be there.
'''
logging function:
takes in input and LOG_FILE and appends inpu to the current logging file

'''
def log(inpu):
    if(utlilites.check_input('str',inpu)):
        temp=open(PATH+LOG_FILE,"r+")#should take care of the LOG_FILE not being created
        temp.write(inpu+'\n')
        temp.close()
        #FAIL RETURN TO START!
        return 1
    else:
        return -1

'''
UI
Debugging function while the actual user input child is being generated
'''
def guiMinus():

'''
Creates and returns the log file
'''
def setLogFile(path):
    ret = -1
    if(utlilites.check_input('str',path)):
        nam = 'log'+ time.strftime('%d_%h_%m')
        ret= nam
    temp=open(path+nam,'w+')
    temp.close()
    return ret

'''
parses the settings file, returns it as array
'''
def parse_settings(path, name):
    current_setting=''
    if(utlilites.check_input('str',path)):
        if(utlilites.check_input('str',name)):
            file = open(path+name,'r')
            for i in file.read():
                if current_setting = '':
                    current_setting = i[:-1]
                elif current_setting = PLACEHOLDER:
                    #do stuff
                elif current_setting = PLACEHOLDER:
                    #do stuff
                else:
                    log(LOG_FILE, 'Unknown Setting')
