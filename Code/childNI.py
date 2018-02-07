""" handles incoming network traffic

Classes: None
Exceptions:
Functions:
main --
net_in --
"""

import socket
import sys

#from scapy.all import *
import sqlite3
import os
#import tShark
import utilities
import pcaphandler

#TODO change packets.db to a constant that can be set by the user
#TODO change put_pcaps_here to a constant, possibly not necessary
#TODO need to make pcaphandler have segregated functions
#TODO need to make main mesh better with pcaphandler
#TODO run stress test
def main():
    """
    Checks for type and returns the input, otherwise returns an error message
    """
    keep_going = True
    conn = sqlite3.connect('packets.db')
    packetNum = 0
    sql = conn.cursor()
    generateDB(sql)
    my_var = 0
    work_dir = os.getcwd()
    tgt_dir = os.path.dirname(work_dir)
    pcap_dir = ''
    db_already_made = False
    if os.basename(packets.db):
        db_already_made = True
    for dir_name in os.walk(tgt_dir):
        if 'put_pcaps_here' == os.path.basename(dir_name[0]):
            pcap_dir = dir_name[0]

    #Here is where database stuff begins
    conn= sqlite3.connect('packets.db')
    cur = conn.cursor()
    if not db_already_made:
        generateDB(sql)
    numberChanged = pcaphandler.split()
    #Pcaps in put pcaps here should be moved or deleted
    #Will start with moved
    #if there is more than one file, move it to processed
    #only moves files
    if numberChanged > 0:
        for i in os.listdir(pcap_dir)::
            if os.path.isfile(i):
                os.rename(os.pcap_dir+'\\'+i,os.getcwd()+'\\processed\\'+i)
    flows = pcaphandler.getSqlData()
    for dir_name in os.listdir(pcap_dir):
        if os.path.isdir(dir_name) and not dir_name == "processed":
            os.rename(pcap_dir+'\\'+dir_name,pcap_dir+'\\processed\\'+dir_name) #may not be stable
    for flow in flows:
        addPacket(flow, cur)
    #testing success
    printSqlDatabase()


def net_in(host, port):
    """
    TODO fill in docstring
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    #sock.connect((host, port))
    #sock.shutdown(socket.SHUT_WR)
    received = 0
    while True:
        print('Listening at', sock.getsockname())
        soc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('Socket connects', soc.getsockname(), 'and', soc.getpeername())
        message = soc.recv(16)
        message_length = int(message.split()[1].decode('utf-8'))
        return_message = message
        rest = soc.recv(message_length)
        return_message += rest
        print_message = return_message.decode('utf-8')
        print('The incoming sixteen-octet message says', print_message)
        soc.sendall(return_message)
        soc.close()
        print('  Reply sent, socket closed\n')

#main()

#scapy

def generateDB(conn):
    conn.execute('''CREATE TABLE flows
             (flowNum integer primary key,
              timest real,
              portIn integer,
              portOut integer,
              flowReference text)''')
    conn.execute('''CREATE TABLE flags
             (flagNum integer primary key,
             flag text)''')
    conn.execute('''CREATE TABLE connection
             (flagDiscNumber integer primary key,
             flowNum integer references flows(flowNum),
             flagNum integer references flags(flagNum))''')

'''
need to know
payload, in/out,

build flows, sepirated by time
'''

#flows is the pointer to to csv that is already opened
#might want to change in the future
def addPacket(flows, conn, cur):
    #parse

    #must be last most recent packet, every one following is appended
    cur.execute("SELECT flowNum FROM flows ORDER BY flowNum DESC LIMIT 1")
    recent=cur.fetchall()
    if len(recent) == 0:
        recent=0
    else:
        recent = recent[0]
    flo = open(flows,'r+')
    lines = flo.readlines()
    flo.close()
    dataGroups=[]
    flags = []
    for i in lines:
        fields = i.split(',')
        temp=(fields[0],fields[1],fields[2],fields[3])
        dataGroups.append(temp)
        tem = []
        for j in range(4,len(fields)):
            if not fields[j] == '' and not fields[j] == '\n':
                tem.append(fields[j])
        flags.append(tem)
    flagPacketRelationship=addFlags(flags,conn,cur)

    #print(flagPacketRelationship)
    flagSub=[]
    for packet in flagPacketRelationship:
        for flag in packet:
            flagSub.append((recent, flag))
        recent = recent + 1
    #print(flagSub)
    for dataGroup in range(0,len(dataGroups)):
        cur.execute("INSERT INTO flows(timest, portIn, portOut, flowReference) VALUES (?, ?, ?, ?)", dataGroups[dataGroup])
        #for flag in flagSub[dataGroup]:
        #    print(flag)
        cur.execute("INSERT INTO connection(flagNum,flowNum) VALUES (?, ?)", flagSub[dataGroup])
    conn.commit()
#I think htis is how it works?
#in order of input, returns the flags and how they're related
def addFlags(flags,conn, cur):
    flagNumbers=[]
    for packet in flags:
        packetFlags=[]
        for flag in packet:
            cur.execute("SELECT * FROM flags WHERE ? = flag", (flag,))
            comp=cur.fetchall()
            if len(comp) == 0:
                cur.execute("INSERT INTO flags(flag) VALUES (?)", (flag,))
                cur.execute("SELECT flagNum FROM flags ORDER BY flagNum DESC LIMIT 1")
                temp=cur.fetchall()
                packetFlags.append(temp[0])
            else:
                cur.execute("SELECT flagNum FROM flags WHERE ? = flag", (flag,))
                check = cur.fetchall()
                if not check in packetFlags:
                    cur.execute("SELECT flagNum FROM flags WHERE ? = flag", (flag,))
                    temp=cur.fetchall()
                    packetFlags.append(temp[0])
        for Flag in packetFlags:
            flagNumbers.append(Flag)
    conn.commit()
    return flagNumbers

#finds flows with a given port in
def searchSqlFlowsPortIn(inp,cur):
    cur.execute('SELECT flowReference FROM flows where portIn = ?',(inp,))
    ret = cur.fetchall()
    return ret

#finds flows with a given port out
def searchSqlFlowsPortOut(inp,cur):
    cur.execute('SELECT flowReference FROM flows where portOut = ?',(inp,))
    ret = cur.fetchall()
    return ret

#Finds flows with a minimum number of flags sorted by the time incoming
def searchSqlFlowsFlags(inp, cur):
    cur.execute('SELECT flowReference, flag FROM flows INNER JOIN connection on flows.flowNum = connection.flowNum INNER JOIN flags on flags.flagNum = connection.flagNum ORDER BY timest DESC LIMIT ?',(inp,))
    ret = cur.fetchall()
    return ret

#finds flows with a given port in and at least 1 flag
def searchSqlPortInWithFlags(inp, cur):
    cur.execute('SELECT flowReference, flag FROM flows INNER JOIN connection on flows.flowNum = connection.flowNum INNER JOIN flags on flags.flagNum = connection.flagNum where portIn = ? ORDER BY timest',(inp,))
    ret = cur.fetchall()
    return ret

#finds flows with a given port out and at least 1 flag
def searchSqlPortOutWithFlags(inp, cur):
    cur.execute('SELECT flowReference, flag FROM flows INNER JOIN connection on flows.flowNum = connection.flowNum INNER JOIN flags on flags.flagNum = connection.flagNum where portOut = ? ORDER BY timest',(inp,))
    ret = cur.fetchall()
    return ret

#allows generalized queries on database
def searchSql(inp,cur):
    cur.execute(inp)
    ret = cur.fetchall()
    return ret

def getCur():
    conn= sqlite3.connect('packets.db')
    cur = conn.cursor()
    return cur

def printSqlDatabase():
    conn= sqlite3.connect('packets.db')
    sql = conn.cursor()
    #flow='testDB.csv'
    #addPacket(flow,conn,sql)
    flows = searchSql('SELECT * FROM flows',sql)
    relationships = searchSql('SELECT * FROM connection',sql)
    flags = searchSql('SELECT * FROM flags',sql)
    add = ''
    a = open('flows.csv','w+')
    for i in flows:
        for j in i:
            add = add + str(j) + ','
        add = add + '\n'
    a.write(add)
    a.close()
    add = ''
    a = open('relationships.csv','w+')
    for i in relationships:
        for j in i:
            add = add + str(j) + ','
        add = add + '\n'
    a.write(add)
    a.close()
    add = ''
    a = open('flags.csv','w+')
    for i in flags:
        for j in i:
            add = add + str(j) + ','
        add = add + '\n'
    a.write(add)
    a.close()

def testDB():
    conn= sqlite3.connect('packets.db')
    sql = conn.cursor()
    #generateDB(sql)
    #flow='testDB.csv'
    #addPacket(flow,sql)
    test1 = searchSqlFlowsPortIn('8081',sql)
    test2 = searchSqlFlowsPortOut('35934',sql)
    test3 = searchSqlFlowsFlags('2',sql)
    test4 = searchSql('SELECT * FROM flows',sql)
    print(test1)
    if len(test1) == 3:
        print('Ports In: Pass')
    else:
        print('Ports In: Fail')
    print(test2)
    if len(test2) == 1:
        print('Ports Out: Pass')
    else:
        print('Ports Out: Fail')
    print(test3)
    if len(test3) == 2:
        print('Flags found: Pass')
    else:
        print('Flags found: Fail')
    print(test4)
    if len(test4) == 5:
        print('General Search: Pass')
    else:
        print('General Search: Fail')
    conn.close()
