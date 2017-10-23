'''
utilities.py

stores any functions that should be used across all systems in a local manner
'''

#imports
import subprocess
# struct target
'''
Generalized parser
sort of implemented in main, might need to differentiate someway in the future
keeping because no real reason to remove
'''
def parser(path, inpu):
    length = 0
    seconds = 0
    file = open(path+inpu)
    use = ''
    for i in file():
        use = use + i.read
    return inpu

'''
checks that the input matches the expected type
generated by an explicit declairaiton of the desired system
for example 'str' or list[]
'''
def check_input(expected, recieved):
    ret = False
    if isinstance(expected) == isinstance(recieved):
        ret = True

    return ret


'''
Creator: Tate Bowers
Input: process name
Output: connection to child input/output
This function takes in a file to run and runs it, passing in the output and input to a location that you can use
TODO figure out how to properly sync error logging
inp

'''
def create_child(inp, other_arguments):
    ret = -1
    if check_input('str', inp):
        if check_input('str', other_arguments): #can be a str or array, probably should be str
            run = 'python '+inp+'.py '+other_arguments
            try:
                ret = subprocess.Popen(run, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    #send stdout to buffer, to write to log
            except ChildProcessError:
                print('scream and run')
                #run debug process and try again later
                #logBuffer = logBuffer + "UI Error: Failed to init"
                #try this
                    #try
                    #except ChildProcessError
                    #except as otr: again
                #seems like it would be a good idea to push this to a function.
            #except:
                #something else went wrong, try to make better
                #logBuffer=logBuffer+"UI Error: " + sys.exc_info()[0]#think this is the syntax

    return ret
