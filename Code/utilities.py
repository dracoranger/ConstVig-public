#stores any functions that should be used across all systems in a local manner

#Classes: None
#Exceptions:
#Functions:
#parser -- parses data from files
#check_input -- checks whether the input is of the correct type
#create_child -- runs the file (will be a child process) given as input
#comm_out -- sends communications out through ports
#comm_in -- creates a listener
#read_from_server -- prints messages received from server
#network_out -- actual process for outgoing network communications
#network_in -- actual process for incoming network communications


import subprocess
import socket
import os
import configparser
# struct target

def check_input(expected, recieved):
    #checks whether input is of the expected type.

    #Summary of behavior: Checks that the received input type matches
    #the type that was expected (which is explicitly given in the input.
    #For example, received "hello world" with type int would return false.
	#Arguments: the type that is expected and what was actually receieved
    #Return values: boolean stating whether the input types matched
    #Side effects:
    #Exceptions raised:
    #Restrictions on when it can be called:
    #Creator: Tate Bowers

    return isinstance(recieved, type(expected))

def create_child_gen(run):
    #creates a child that is given in fileName.
    #Same as above except can run more than python files
    #depends on user properly uploading a run[] with the reuqired arguements

    ret = -1
    temp = ''
    if check_input(temp, run):
        try:
            ret = subprocess.Popen(run, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

                #should run to completion, probably should pipe output to a log file
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


def generate_default_config():
    config = configparser.ConfigParser()
    config['dad'] = {'rounds' : '100',
                     'round_length':'300',
                     'PATH':os.getcwd()+'\\dad.py',
                     'death_limit':'3',
                     'time_between_check':'5',
                     'LOG_FILE':'main.log',
                     'CHILD_NUM':'2',
                     '0':'0'
                    }
    config['NetworkIn'] = {
        '''#Premade SQL queries are as follows\n
        #searchSqlFlowsPortIn(\'port as string\',getCur()) - shows flows matching port in\n
        #searchSqlFlowsPortOut(\'port as string\',getCur()) - shows flows matching port out\n
        #searchSqlFlowsFlags(\'minimun number of flags as string\',getCur()) - finds flows that have a minimum number of flags\n
        #searchSqlPortInWithFlags(\'port as string\',getCur()) - shows flows that have flags present given the port in\n
        #searchSqlPortOutWithFlags(\'port as string\',getCur()) - shows flows that have flags present given the port out\n
        #searchSql(inp,cur) - generalized search function on sql.  Feeds query directly to database, so needs to be a valid sql query''':'',
        'pcapFolder': os.getcwd()[:(os.getcwd().rfind('\\')-len(os.getcwd()))]+'\\'+'put_pcaps_here'
        }
    config['NetworkOut'] = {
        '''#The range of IPs that should be targeted should be in the format XXX.XXX.XXX.XXX/XX with the first IP and the subnet mask\n
        #Separate the ports to be attacked with a ,\n
        #Both paths are defaults, it grabs the current working directory when it is run, then appends chaff and attack.''':'',
        'ipRange':'192.168.1.0/24',
        'ports': '23,24,35',
        'SUBMIT_FLAG_IP':'192.168.1.1',
        'SUBMIT_FLAG_PORT':'9001',
        'PATH_CHAFF':os.getcwd()+'\\chaff',
        'PATH_ATTACK':os.getcwd()+'\\attacks'
        }
    config['Attacks'] = {
        '''#Format should be the file name followed by the command line argument to run it.\n
        #Store the attacks in the PATH_ATTACK directory\n#add -i to have it iterate through the items in ipRange\n
        #add -p to iterate through the ports\n#add -f to add the ip address and port of where the flag should be submitted in the format SUBMIT_FLAG_IP + \' \' + SUBMIT_FLAG_PORT''':'',
        "hello_world.py" : "python hello_world.py",
        "looper.py" : "python looper.py"
        }
    config['Chaff'] = {
        '''#Format should be the file name followed by the command line argument to run it.\n#Store the chaff in the PATH_CHAFF directory\n
        #add -i to have it iterate through the items in ipRange\n#add -p to iterate through the ports\n
        #add -f to add the ip address and port of where the flag should be submitted in the format SUBMIT_FLAG_IP + \' \' + SUBMIT_FLAG_PORT''':'',
        }
    with open('constvig.conf','w') as configfile:
        config.write(configfile)

def parse_config(section):
    config = configparser.ConfigParser()
    #taken from python.org wiki
    def config_section_map(section):

        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    config.read('constvig.conf')
    ret = config_section_map(section)
    return ret

def submit_flag(ip, port, data):
    reply = -1
    if check_input(data, b'bytes'):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(data)
        sock.close()
        reply = sock.recv(512).decode()
    return reply
