import time
import utilities
'''
Classes:
CHILD -- each child is a processes, e.g. NetIn (NI) that serves a specific purpose.
Exceptions:
Functions:
main -- loops through the children, checking for deaths and restarting when appropriate
'''

class CHILD:
    '''
    Summary of behavior: tracks each child and information pertinent to the child
    Public methods: get_name, recreate_subprocess
    Instance variables: Name
    Creator: Tate Bowers
    '''
    def __init__(self, nam):
        self.name = nam
        self.process = utilities.create_child_gen('python '+ self.name +'.py')

    def get_name(self):
        return self.name

    def recreate_subprocess(self):
        #kills and then creates the child process
        self.process.kill()
        self.process = utilities.create_child_gen('python '+ self.name +'.py')

def main():
    '''
    Summary of behavior: starts, restarts, and manages the child processes
    Arguments: None
    Return values:
    Side effects: child processes launched and monitored for success
    Exceptions raised:
    Restrictions on when it can be called: None
    '''
    config = utilities.parse_config('dad')
    round_length = int(config['round_length'])
    total_rounds = int(config['total_rounds'])
    time_between_check = int(config['time_between_check'])
    log_file = config['log_file']

    utilities.log_data(log_file, 'Began operations at '+str(time.time())+'\n')

    child = CHILD('ChildNO')

    for i in range(0, total_rounds):
        time_start = time.time()
        while time.time() - time_start < round_length:
            print(str(time.time()-time_start))
            if utilities.check_input(child.process.poll(), 1):
                if child.process.poll() == 0:
                    response = str(child.process.communicate())
                    utilities.log_data(log_file, '%s success: %s at %s\n' %
                                       (child.get_name(), response, str(time.time())))
                else:
                    response = str(child.process.communicate())
                    utilities.log_data(log_file, '%s failure: %s at %s\n' %
                                       (child.get_name(), response, str(time.time())))
                    print(child.get_name()+response)
            elif child.process.poll() is None:
                utilities.log_data(log_file, '%s Ongoing at %s\n' %
                                   (child.get_name(), str(time.time())))
            else:
                print('please look up what happens if subprocess.poll() does not return 1 or None')
            time.sleep(time_between_check)
        if child.process.poll() is None:
            print(child.get_name()+' on going: possibly too many files being launched')
        child.recreate_subprocess()
        print('round '+str(i)+' complete')
    utilities.log_data(log_file, 'Ended operations at %s\n' %
                       (str(time.time())))
    print('fully complete')

#Runs the main function
print('starting '+str(time.time()))
main()
