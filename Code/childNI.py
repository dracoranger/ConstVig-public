import socket
import sys
import sqlite3
import os
import csv
import utilities
import pcaphandler

#TODO change packets.db to a constant that can be set by the user
#TODO change put_pcaps_here to a constant, possibly not necessary
#TODO need to make pcaphandler have segregated functions
#TODO need to make main mesh better with pcaphandler
#TODO run stress test
def main():

    #Checks for type and returns the input, otherwise returns an error message
    keep_going = True
    #Here is where database stuff begins
    db_already_made = False
    if 'packets.db' in os.listdir():
        db_already_made = True
    conn = sqlite3.connect('packets.db')
    cur = conn.cursor()
    if not db_already_made:
        generateDB(cur)

    work_dir = os.getcwd()
    tgt_dir = os.path.dirname(work_dir)
    pcap_dir = ''

    for dir_name in os.walk(tgt_dir):
        if 'put_pcaps_here' == os.path.basename(dir_name[0]):
            pcap_dir = dir_name[0]
    numberChanged = pcaphandler.split()
    # Pcaps in put pcaps here should be moved or deleted
    # Will start with moved
    # if there is more than one file, move it to processed
    # only moves files
    if numberChanged > 0:
        for i in os.listdir(pcap_dir):
            if os.path.isfile(i):
                os.rename(pcap_dir+'\\'+i,os.getcwd()+'\\processed\\'+i)
    flows = pcaphandler.getSqlData()
    for dir_name in os.listdir(pcap_dir):
        if os.path.isdir(dir_name) and not dir_name == "processed":
            os.rename(pcap_dir+'\\'+dir_name,pcap_dir+'\\processed\\'+dir_name)
            # TODO may not be stable
    for flow in flows:
        addPacket(flow, conn, cur)
    # testing success
    os.chdir('C:\\Users\\T\\Documents\\GitHub\\ConstVig\\Code')
    printSqlDatabase()

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

#need to know
#payload, in/out,
#build flows, sepirated by time


#flows is the pointer to to csv that is already opened
#might want to change in the future
def addPacket(flows, conn, cur):
    #parse

    #must be last most recent packet, every one following is appended
    cur.execute("SELECT flowNum FROM flows ORDER BY flowNum DESC LIMIT 1")
    recent = cur.fetchall()
    if len(recent) == 0:
        recent = 0
    else:
        recent = recent[0]
    flo = open(flows, 'r+')
    lines = flo.readlines()
    flo.close()
    dataGroups = []
    flags = []
    for i in lines:
        fields = i.split(',')
        temp = (fields[0], fields[1], fields[2], fields[3])
        dataGroups.append(temp)
        tem = []
        for j in range(4, len(fields)):
            if not fields[j] == '' and not fields[j] == '\n':
                tem.append(fields[j])
        flags.append(tem)
    flagPacketRelationship = addFlags(flags, conn, cur)

    #print(flagPacketRelationship)
    flagSub = []
    for packet in flagPacketRelationship:
        for flag in packet:
            flagSub.append((recent, flag))
        #recent = recent + 1
    #print(flagSub)
    #TODO can I just do a full insert?
    #Fast enough now, but not sure if I need to do iterate
    for dataGroup in range(0, len(dataGroups)):
        cur.execute("""INSERT INTO flows(timest, portIn, portOut, flowReference)
        VALUES (?, ?, ?, ?)""", dataGroups[dataGroup])
        for flag in flagSub[dataGroup]:
            print(flag)
        #Note, need to be careful if flags do not exist
        cur.execute("INSERT INTO connection(flagNum,flowNum) VALUES (?, ?)",
                    flagSub[dataGroup])
    conn.commit()
#I think htis is how it works?
#in order of input, returns the flags and how they're related
def addFlags(flags,conn, cur):
    flagNumbers = []
    for packet in flags:
        packetFlags = []
        for flag in packet:
            cur.execute("SELECT * FROM flags WHERE ? = flag", (flag,))
            comp = cur.fetchall()
            if comp.isEmpty():
                cur.execute("INSERT INTO flags(flag) VALUES (?)", (flag,))
                cur.execute("SELECT flagNum FROM flags ORDER BY flagNum DESC LIMIT 1")
                temp = cur.fetchall()
                packetFlags.append(temp[0])
            else:
                cur.execute("SELECT flagNum FROM flags WHERE ? = flag", (flag,))
                check = cur.fetchall()
                if not check in packetFlags:
                    cur.execute("SELECT flagNum FROM flags WHERE ? = flag", (flag,))
                    temp = cur.fetchall()
                    packetFlags.append(temp[0])
        for flag in packetFlags:
            flagNumbers.append(flag)
    conn.commit()
    return flagNumbers

#finds flows with a given port in
def searchSqlFlowsPortIn(inp,cur):
    cur.execute('SELECT flowReference FROM flows where portIn = ?', (inp,))
    return cur.fetchall()

#finds flows with a given port out
def searchSqlFlowsPortOut(inp,cur):
    cur.execute('SELECT flowReference FROM flows where portOut = ?', (inp,))
    return cur.fetchall()

#Finds flows with a minimum number of flags sorted by the time incoming
def searchSqlFlowsFlags(inp, cur):
    cur.execute('''SELECT flowReference, flag FROM flows
    INNER JOIN connection on flows.flowNum = connection.flowNum
    INNER JOIN flags on flags.flagNum = connection.flagNum
    ORDER BY timest DESC LIMIT ?''', (inp,))
    return cur.fetchall()

#finds flows with a given port in and at least 1 flag
def searchSqlPortInWithFlags(inp, cur):
    cur.execute('''SELECT flowReference, flag FROM flows
    INNER JOIN connection on flows.flowNum = connection.flowNum
    INNER JOIN flags on flags.flagNum = connection.flagNum
    where portIn = ? ORDER BY timest''', (inp,))
    return cur.fetchall()

#finds flows with a given port out and at least 1 flag
def searchSqlPortOutWithFlags(inp, cur):
    cur.execute('''SELECT flowReference, flag FROM flows
    INNER JOIN connection on flows.flowNum = connection.flowNum
    INNER JOIN flags on flags.flagNum = connection.flagNum
    where portOut = ? ORDER BY timest''', (inp,))
    return cur.fetchall()

#allows generalized queries on database
def searchSql(inp,cur):
    cur.execute(inp)
    return cur.fetchall()

def getCur():
    conn = sqlite3.connect('packets.db')
    return conn.cursor()

def printSqlDatabase():
    conn = sqlite3.connect('packets.db')
    cur = conn.cursor()
    #flow='testDB.csv'
    #addPacket(flow,conn,sql)
    flows = searchSql('SELECT * FROM flows', cur)
    relationships = searchSql('SELECT * FROM connection', cur)
    flags = searchSql('SELECT * FROM flags', cur)
    with open('flows.csv', 'w+') as flows:
        writer = csv.writer(flows)
        writer.writerows(flows)
    with open('relationships.csv', 'w+') as relationships:
        writer = csv.writer(relationships)
        writer.writerows(relationships)
    with open('flags.csv', 'w+') as flags:
        writer = csv.writer(flags)
        writer.writerows(flags)
