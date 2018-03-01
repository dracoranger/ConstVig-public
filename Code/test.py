import pytest
import ipaddress
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
    #will need to do some manual stuff
    #test
