import pytest
import ipaddress
import os
import dad
import childNO
import childNI
import utilities

dictionA = utilities.parseConfig('Attacks')
dictionC = utilities.parseConfig('Chaff')
dictionNO=utilities.parseConfig('NetworkOut')
PATH_ATTACK = dictionNO['path_attack']
PATH_CHAFF = dictionNO['path_chaff']
IP_RANGE =  list(ipaddress.ip_network(dictionNO['iprange']).hosts())
PORTS = dictionNO['ports'].split(',')
SUBMIT_FLAG_PORT = dictionNO['submit_flag_port']
SUBMIT_FLAG_IP = dictionNO['submit_flag_ip']

def check_NO_log():
    with open('attack.log','r+') as log:
        dat = log.readlines()
    return dat

def reset_database():
    starting_locl = os.getcwd()
    os.remove('packets.db')
    os.chdir('..')
    os.chdir('put_pcaps_here')
    locl_path = os.getcwd()
    for i in os.listdir('.'):
        if os.path.isfile(i):
            comp=i.split('.')
            if comp[1]=='csv':
                os.remove(i)
    os.chdir('processed')
    for dir_name in os.listdir(os.getcwd()):
        if os.path.isdir(dir_name):
            os.chdir(dir_name)
            for fil in os.listdir(os.getcwd()):
                os.remove(fil)
            os.chdir('..')
            os.rmdir(dir_name)
        elif os.path.isfile(dir_name):
            os.rename(os.getcwd()+'\\'+dir_name, locl_path+'\\'+dir_name)
    os.chdir(starting_locl)
    childNI.main()

def main():

    #network out
    #Ignoring ongoing.  Might need to offer ability to kill
    #test flag replacement
    #test ip replacement
    #test port replacement
    #test both
    #test completion <-sort of already done.  Check log?
    attackDictionary={}
    assert childNO.run_processes("Attacks", attackDictionary, PATH_ATTACK, "attack.log") == ['python hello_world.py','python failure.py']
    results = check_NO_log()
    assert results[:-1] == "hello_world.py success: (b'Hello world!\r\n', None)"
    assert results[:-2] == "failure.py failure: (b'trying an impossibility!\r\n', None)"
    assert results[:-3] == ''#flag result
    assert results[:-4] == ''#ip result
    assert results[:-5] == ''#port result
    assert results[:-6] == ''#both result

    #network in
    #waiting on regex for flag
    reset_database()
    #test
    cur = childNI.getCur()
    test1 = childNI.searchSqlFlowsPortIn('port value',cur)
    test2 = childNI.searchSqlFlowsPortOut('port value',cur)
    test3 = childNI.searchSqlFlowsFlags('number',cur) #probably need to change this with tshark shift
    test4 = childNI.searchSqlPortInWithFlags('port value',cur)
    test5 = childNI.searchSqlPortOutWithFlags('port value',cur)
    assert len(test1) == 'x'
    assert len(test2) == 'x'
    assert len(test3) == 'x'
    assert len(test4) == 'x'
    assert len(test5) == 'x'

    #dad
