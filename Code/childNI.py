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

def main():
    """
    Checks for type and returns the input, otherwise returns an error message
    """
    keep_going = True
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect(('localhost', 15551))
    #recieved = sock.recv(1024).decode()
    conn = sqlite3.connect('packets.db')
    packetNum = 0
    sql = conn.cursor()
    #listener, sock = utilities.comm_in(9751)
    #while keep_going:
        #commented out print() and changed input()
        #print('NI')
        #try:
    #    able = bytes('Temp val', 'utf-8')#sys.stdin.readline(5)
        #if utilities.check_input((bytes), able):
        #    sock.send(able.encode())
            #utilities.comm_out(able, sock)
        #except EOFError:
        #    print('no data supplied')
    #sock.close()
    #listener.join()
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
    ports, timestamp, data = parser(inp)

    ret = analyzer_ports(ports,timestamp)
    ret = ret + analyzer_data(data,timestamp)

def analyzer_data(dat, timestamp):
    '''
        >>>analyzer_data()
        [jklasdnvhiuopq[n, n+20, n+40, n+80, n+100],qiuopnjvpasewrnjkaxpjbnadfsjiopea[n+5,n+10,n+15],...]
    '''

def analyzer_ports(ports, timestamp):
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
              timestamp real,
              portIn integer,
              portOut integer,
              protocol integer,
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

#might want to do packets at once, since that is generally safer
#rewriting it to do every packet at once
def addPacket(flow, conn):
    #parse
    time = 0
    portIn = 1
    portOut = 1
    protocol = 17
    data="Flow1234.pcap" #temp value
    flags = [['71-28-71'],['717-218-721']]#one per packet?

    #must be last most recent packet, every one following is appended
    conn.execute("SELECT flowNum FROM flows ORDER BY flowNum DESC LIMIT 1")
    recent=conn.fetchall()
    if len(recent) == 0:
        recent=0
    else:
        recent = recent[0]

    dataGroups = [(time,portIn,portOut,protocol,data),
                (time+1,portIn+1,portOut+1,protocol+1,data)
                ]

    flagPacketRelationship=addFlags(flags,conn)
    flagSub=[]
    for packet in flagPacketRelationship:
        for flag in packet:
            flagSub.append((recent, flag))
        recent = recent + 1
    print(flagSub)


    for dataGroup in range(0,len(dataGroups)):
        conn.execute("INSERT INTO flows(timestamp, portIn, portOut, protocol, flowReference) VALUES (?, ?, ?, ?, ?)", dataGroups[dataGroup])
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
                conn.execute("SELECT flagNumber FROM flags WHERE ? = flag", (flag,))
                check = conn.fetchall()
                if not check in packetFlags:
                    conn.execute("SELECT flagNumber FROM flags WHERE ? = flag", (flag,))
                    temp=conn.fetchall()
                    packetFlags.append(temp[0])
        for packetFlag in packetFlags:
            flagNumbers.append(packetFlag)
    return flagNumbers

def searchSqlFlowsPortIn(inp,conn):
    conn.execute('SELECT * FROM flows where portIn = ?',inp)
    ret = conn.fetchall()
    print(ret)

def searchSqlFlowsPortOut(inp,conn):
    conn.execute('SELECT * FROM flows where portOut = ?',inp)
    ret = conn.fetchall()
    print(ret)

def searchSqlFlowsFlags(inp, conn):
    conn.execute('SELECT flowReference, flag FROM flows INNER JOIN connection on flows.flowNum = connection.flowNum INNER JOIN flags on flags.flagNum = connection.flagNum ORDER BY timestamp DESC LIMIT ?',inp)
    ret = conn.fetchall()
    print(ret)

def searchSql(conn, inp):
    conn.execute(inp)
    ret = conn.fetchall()
    print(ret)

def testDB():
    conn=main()
    generateDB(conn)
    flow=open('flows.csv','r+')
    addPacket(flow,conn)
    if searchSqlFlowsPortIn('80',conn) == '':
        print('Ports In: Pass')
    else:
        print('Ports In: Fail')
    if searchSqlFlowsPortOut('80',conn) == '':
        print('Ports Out: Pass')
    else:
        print('Ports Out: Fail')
    if searchSqlFlowsFlags('80',conn) == '':
        print('Flags found: Pass')
    else:
        print('Flags found: Fail')
    if searchSql('SELECT * FROM flows') == '':
        print('General Search: Pass')
    else:
        print('General Search: Fail')
