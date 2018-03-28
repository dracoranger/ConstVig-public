import pytest
import ipaddress
import os
#import dad
import childNO
import childNI
import utilities
import difflib

dictionA = utilities.parse_config('Attacks')
dictionC = utilities.parse_config('Chaff')
dictionNO=utilities.parse_config('NetworkOut')
PATH_ATTACK = dictionNO['path_attack']
PATH_CHAFF = dictionNO['path_chaff']
IP_RANGE =  list(ipaddress.ip_network(dictionNO['iprange']).hosts())
PORTS = dictionNO['ports'].split(',')
SUBMIT_FLAG_PORT = dictionNO['submit_flag_port']
SUBMIT_FLAG_IP = dictionNO['submit_flag_ip']

comparisons = ["both.py success: (b\"Namespace(ip=[\'192.168.1.0\'], p=[\'23\'])\\r\\n\", None)","","flag.py success: (b\"Namespace(f=[\'192.168.1.1,9001\'])\\r\\n\", None)","hello_world.py success: (b\'Hello world!\\r\\n\', None)","ip.py success: (b\"Namespace(ip=[\'192.168.1.0\'])\\r\\n\", None)","","port.py success: (b\"Namespace(p=[\'23\'])\\r\\n\", None)"]

def check_NO_log(val):
    with open('attack.log','r+') as log:
        dat = log.readlines()
    checker = True
    for i in range(0,len(dat[val][:-1])-1):
        if(dat[val][i] != comparisons[val][i]):
            checker = False
    return checker

def test():
    return True

def reset_database():
    starting_locl = os.getcwd()
    if 'packets.db' in os.listdir():
        os.remove('packets.db')
    os.chdir('..')
    os.chdir('put_pcaps_here')
    locl_path = os.getcwd()
    for i in os.listdir('.'):
        if os.path.isfile(i):
            comp = i.split('.')
            if comp[-1] == 'csv':
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
    attackDictionary={}
    childNO.run_processes("Attacks", attackDictionary, PATH_ATTACK, "attack.log")
    print('Functional testing platform is: ' + str(test() is True))
    assert test() == True
    print('Functional Port alone is:  ' + str(check_NO_log(-7) is True))
    assert check_NO_log(-7) is True#both result
    print('Functional IP alone is:  ' + str(check_NO_log(-5) is True))
    assert check_NO_log(-5) is True#flag result
    print('Functional HelloWorld is: ' + str(check_NO_log(-4) is True))
    assert check_NO_log(-4) is True
    print('Functional Flag sending is: ' + str(check_NO_log(-3) is True))
    assert check_NO_log(-3) is True#ip result
    print('Functional both IP and Port is: ' + str(check_NO_log(-1) is True))
    assert check_NO_log(-1) is True#port result

    reset_database()
    cur = childNI.getcur()
    test1 = childNI.search_sql_flows_port_in('"4280"',cur)
    test2 = childNI.search_sql_flows_port_out('"48724"',cur)
    print('Functional find flags given port in is: ' + str(len(test1) == 30))
    assert len(test1) == 30
    print('Functional find flags given port out is: ' + str(len(test1) == 30))
    assert len(test2) == 1
main()
