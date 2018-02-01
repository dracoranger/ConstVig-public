""" handles incoming network traffic

Classes: None
Exceptions:
Functions:
main --
net_in --
"""

import socket
import sys
import utilities
#from scapy.all import *
import sqlite3
import os
#import tShark

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
    for dir_name in os.walk(tgt_dir):
        if 'put_pcaps_here' == os.path.basename(dir_name[0]):
            pcap_dir = dir_name[0]

    #while(my_var < 20):
    #    tShark
    #
        #enters metadata into database
    #    my_var +=1
    return sql


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

def analyzer(inp):
    '''
        >>>analyzer()
        return [80[n, n+20, n+40, n+80, n+100],7558[n+5,n+10,n+15],...],[jklasdnvhiuopq[n, n+20, n+40, n+80, n+100],qiuopnjvpasewrnjkaxpjbnadfsjiopea[n+5,n+10,n+15],...]
    '''
    ports, timest, data = parser(inp)

    ret = analyzer_ports(ports,timest)
    ret = ret + analyzer_data(data,timest)

def analyzer_data(dat, timest):
    '''
        >>>analyzer_data()
        [jklasdnvhiuopq[n, n+20, n+40, n+80, n+100],qiuopnjvpasewrnjkaxpjbnadfsjiopea[n+5,n+10,n+15],...]
    '''

def analyzer_ports(ports, timest):
    '''
        >>>analyzer_ports()
        [80[n, n+20, n+40, n+80, n+100],7558[n+5,n+10,n+15],...]
    '''

def parser(inp):
    '''
        >>>parser()
        [80,7558,7558,80,7558,80,7558...],[n, n+5,n+10,n+15,n+20,n+40,n+80],[jklasdnvhiuopq,qiuopnjvpasewrnjkaxpjbnadfsjiopea,qiuopnjvpasewrnjkaxpjbnadfsjiopea,qiuopnjvpasewrnjkaxpjbnadfsjiopea,jklasdnvhiuopq,jklasdnvhiuopq]
    '''

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
def addPacket(flows, conn):
    #parse

    #must be last most recent packet, every one following is appended
    conn.execute("SELECT flowNum FROM flows ORDER BY flowNum DESC LIMIT 1")
    recent=conn.fetchall()
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
    flagPacketRelationship=addFlags(flags,conn)

    #print(flagPacketRelationship)
    flagSub=[]
    for packet in flagPacketRelationship:
        for flag in packet:
            flagSub.append((recent, flag))
        recent = recent + 1
    #print(flagSub)
    for dataGroup in range(0,len(dataGroups)):
        conn.execute("INSERT INTO flows(timest, portIn, portOut, flowReference) VALUES (?, ?, ?, ?)", dataGroups[dataGroup])
        #for flag in flagSub[dataGroup]:
        #    print(flag)
        conn.execute("INSERT INTO connection(flagNum,flowNum) VALUES (?, ?)", flagSub[dataGroup])

#I think htis is how it works?
#in order of input, returns the flags and how they're related
def addFlags(flags,conn):
    flagNumbers=[]
    for packet in flags:
        packetFlags=[]
        for flag in packet:
            conn.execute("SELECT * FROM flags WHERE ? = flag", (flag,))
            comp=conn.fetchall()
            if len(comp) == 0:
                conn.execute("INSERT INTO flags(flag) VALUES (?)", (flag,))
                conn.execute("SELECT flagNum FROM flags ORDER BY flagNum DESC LIMIT 1")
                temp=conn.fetchall()
                packetFlags.append(temp[0])
            else:
                conn.execute("SELECT flagNum FROM flags WHERE ? = flag", (flag,))
                check = conn.fetchall()
                if not check in packetFlags:
                    conn.execute("SELECT flagNum FROM flags WHERE ? = flag", (flag,))
                    temp=conn.fetchall()
                    packetFlags.append(temp[0])
        for Flag in packetFlags:
            flagNumbers.append(Flag)
    return flagNumbers

def searchSqlFlowsPortIn(inp,conn):
    conn.execute('SELECT timest FROM flows where portIn = ?',(inp,))
    ret = conn.fetchall()
    return ret

def searchSqlFlowsPortOut(inp,conn):
    conn.execute('SELECT timest FROM flows where portOut = ?',(inp,))
    ret = conn.fetchall()
    return ret

def searchSqlFlowsFlags(inp, conn):
    conn.execute('SELECT flowReference, flag FROM flows INNER JOIN connection on flows.flowNum = connection.flowNum INNER JOIN flags on flags.flagNum = connection.flagNum ORDER BY timest DESC LIMIT ?',(inp,))
    ret = conn.fetchall()
    return ret

def searchSql(inp,conn):
    conn.execute(inp)
    ret = conn.fetchall()
    return ret

def printSqlDatabase():
    conn= sqlite3.connect('packets.db')
    sql = conn.cursor()
    flows = searchSql('SELECT * FROM flows',sql)
    relationships = searchSql('SELECT * FROM connection',sql)
    flags = searchSql('SELECT * FROM flags',sql)
    print(flows)
    add = ''
    a = open('flows.csv','w+')
    for i in a:
        add = add + i
    a.write(add)
    a.close()
    add = ''
    a = open('relationships.csv','w+')
    for i in a:
        add = add + i
    a.write(add)
    a.close()
    add = ''
    a = open('flags.csv','w+')
    for i in a:
        add = add + i
    a.write(add)
    a.close()

def testDB():
    conn= sqlite3.connect('packets.db')
    sql = conn.cursor()
    generateDB(sql)
    flow='testDB.csv'
    addPacket(flow,sql)
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
