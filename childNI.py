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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 15551))
    recieved = sock.recv(1024).decode()
    conn = sqlite3.connect('packets.db')
    packetNum = 0
    sql = conn.cursor()
    #listener, sock = utilities.comm_in(9751)
    while keep_going:
        #commented out print() and changed input()
        #print('NI')
        #try:
        able = bytes('Temp val', 'utf-8')#sys.stdin.readline(5)
        if utilities.check_input((bytes), able):
            sock.send(able.encode())
            #utilities.comm_out(able, sock)
        #except EOFError:
        #    print('no data supplied')
    sock.close()
    #listener.join()



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

main()

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
    conn.execute('''CREATE TABLE packets
             (packetNum integer primary key,
              timestamp real,
              portIn integer,
              portOut integer,
              flag text,
              timeToLive integer,
              protocol integer,
              source text,
              dest text,
              dataHash text)''')
    conn.execute('''CREATE TABLE flags
             (flagNumber integer primary key,
             flag text)''')
    conn.execute('''CREATE TABLE connection
             (flagDiscNumber integer primary key autoincrement,
             flag text references flags(flag),
             packetNum integer references packets(packetNum))''')

#might want to do packets at once, since that is generally safer
#rewriting it to do every packet at once
def addPacket(packet,conn):
    #parse
    time = 0
    portIn = 1
    portOut = 1
    flags = '01001'
    timeToLive = 1
    protocol = 17
    source = '1.1.1.1'
    dest = '1.1.1.1'
    dataHash = 'text' #do we want to make it so that we keep tract of hashes? Probably not, since it'll probably either change with each flag or will be trivial responses
    flags = [['71-28-71'],['717-218-721']]#one per packet?


    #must be last most recent packet, every one following is appended
    recent = conn.execute("SELECT id FROM packets ORDER BY id DESC LIMIT 1")+1

    dataGroup = [(time,portIn,portOut,flag,timeToLive,protocol,source,dest),
                (time+1,portIn+1,portOut+1,flag,timeToLive+1,protocol+1,source,dest)
                ]

    flagPacketRelationship=addFlags(flags)
    flagSub=[]
    for packet in flagPacketRelationship:
        for flag in packet:
            flagSub.append((recent, flag))
        recent = recent + 1



    conn.execute("INSERT INTO packets VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dataGroup)
    conn.execute("INSERT INTO connection VALUES (?, ?)", flagSub)

#I think htis is how it works?
#in order of input, returns the flags and how they're related
def addFlags(flags,conn):
    flagNumbers=[]
    for packet in flags:
        packetFlags=[]
        for flag in packet:
            if len(conn.execute("SELECT * FROM flags WHERE ? = flag", i) == 0:
                conn.execute("INSERT INTO flags VALUES (?)", i)
                packetFlags.append(conn.execute("SELECT flagNumber FROM flags ORDER BY flagNumber DESC LIMIT 1"))
            else:
                check = conn.execute("SELECT flagNumber FROM flags WHERE ? = flag", i)
                if not check in packetFlags:
                    packetFlags.append(conn.execute("SELECT flagNumber FROM flags WHERE ? = flag", i))
        flagNumber.append(packetFlags)
    return flagNumber
