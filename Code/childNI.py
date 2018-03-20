# handles traffic coming in from the rest of the network

# NAME: Child Network In
# FILE: ConstVig/Code/ChildNI.py
# CLASSES: N/A
# EXCEPTIONS:
# FUNCTIONS:
#     main
#     generate_db
#     addpacket
#     addflags
#     search_sql_flows_port_in
#     search_sql_flows_port_out
#     search_sql_flows_flags
#     search_sql_port_in_with_flags
#     search_sql_port_out_with_flags
#     search_sql
#     getcur
#     print_sql_datbase

import socket
import sys
import os

import csv
import sqlite3

import utilities
import pcaphandler


# TODO change packets.db to a constant that can be set by the user
# TODO change put_pcaps_here to a constant, possibly not necessary
# TODO need to make pcaphandler have segregated functions
# TODO need to make main mesh better with pcaphandler
# TODO run stress test


def main():

    # Checks for type and returns the input,
    # otherwise returns an error message
    keep_going = True
    # Here is where database stuff begins
    db_already_made = False
    if 'packets.db' in os.listdir():
        db_already_made = True
    conn = sqlite3.connect('packets.db')
    cur = conn.cursor()
    if not db_already_made:
        generate_db(cur)

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
    flows = pcaphandler.get_sql_data()
    for dir_name in os.listdir(pcap_dir):
        if os.path.isdir(dir_name) and not dir_name == "processed":
            os.rename(pcap_dir+'\\'+dir_name,pcap_dir+'\\processed\\'
                      +dir_name)
            # TODO may not be stable
    for flow in flows:
        addpacket(flow, conn, cur)
    # testing success
    os.chdir('C:\\Users\\T\\Documents\\GitHub\\ConstVig\\Code')
    print_sql_datbase()


def generate_db(conn):
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


# need to know payload, in/out, build flows, separated by time
# flows is the pointer to to csv that is already opened
# might want to change in the future
def addpacket(flows, conn, cur):
    # parse
    # must be last most recent packet, every one following is appended
    cur.execute("SELECT flowNum FROM flows ORDER BY flowNum DESC LIMIT 1")
    recent = cur.fetchall()
    if len(recent) == 0:
        recent = 0
    else:
        recent = recent[0]
    flo = open(flows, 'r+')
    lines = flo.readlines()
    flo.close()
    data_groups = []
    flags = []
    for i in lines:
        fields = i.split(',')
        temp = (fields[0], fields[1], fields[2], fields[3])
        data_groups.append(temp)
        tem = []
        for j in range(4, len(fields)):
            if not fields[j] == '' and not fields[j] == '\n':
                tem.append(fields[j])
        flags.append(tem)
    flag_packet_relationship = addflags(flags, conn, cur)

    # print(flag_packet_relationship)
    flag_sub = []
    for packet in flag_packet_relationship:
        for flag in packet:
            flag_sub.append((recent, flag))
        # recent = recent + 1
    # print(flag_sub)
    # TODO can I just do a full insert?
    # Fast enough now, but not sure if I need to do iterate
    for dataGroup in range(0, len(data_groups)):
        cur.execute("""INSERT INTO flows(timest, portIn, portOut,
                    flowReference) VALUES (?, ?, ?, ?)""",
                    data_groups[dataGroup]
                    )
        if flag_sub != []:
            for flag in flag_sub[dataGroup]:
                print(flag)
        # Note, need to be careful if flags do not exist
            cur.execute("INSERT INTO connection(flagNum,flowNum)
                        VALUES (?, ?)", flag_sub[dataGroup])
    conn.commit()


# in order of input, returns the flags and how they're related
def addflags(flags,conn, cur):
    flag_numbers = []
    for packet in flags:
        packet_flags = []
        for flag in packet:
            cur.execute("SELECT * FROM flags WHERE ? = flag", (flag,))
            comp = cur.fetchall()
            if comp.isEmpty():
                cur.execute("INSERT INTO flags(flag) VALUES (?)", (flag,))
                cur.execute("SELECT flagNum FROM flags ORDER BY flagNum
                            DESC LIMIT 1")
                temp = cur.fetchall()
                packet_flags.append(temp[0])
            else:
                cur.execute("SELECT flagNum FROM flags WHERE ? = flag",
                            (flag,))
                check = cur.fetchall()
                if not check in packet_flags:
                    cur.execute("SELECT flagNum FROM flags WHERE ? = flag",
                                (flag,))
                    temp = cur.fetchall()
                    packet_flags.append(temp[0])
        for flag in packet_flags:
            flag_numbers.append(flag)
    conn.commit()
    return flag_numbers


# finds flows with a given port in
def search_sql_flows_port_in(inp,cur):
    cur.execute('SELECT flowReference FROM flows where portIn = ?', (inp,))
    return cur.fetchall()


# finds flows with a given port out
def search_sql_flows_port_out(inp,cur):
    cur.execute('SELECT flowReference FROM flows where portOut = ?', (inp,))
    return cur.fetchall()


# Finds flows with a minimum number of flags sorted by the time incoming
def search_sql_flows_flags(inp, cur):
    cur.execute('''SELECT flowReference, flag FROM flows
    INNER JOIN connection on flows.flowNum = connection.flowNum
    INNER JOIN flags on flags.flagNum = connection.flagNum
    ORDER BY timest DESC LIMIT ?''', (inp,))
    return cur.fetchall()


# finds flows with a given port in and at least 1 flag
def search_sql_port_in_with_flags(inp, cur):
    cur.execute('''SELECT flowReference, flag FROM flows
    INNER JOIN connection on flows.flowNum = connection.flowNum
    INNER JOIN flags on flags.flagNum = connection.flagNum
    where portIn = ? ORDER BY timest''', (inp,))
    return cur.fetchall()


# finds flows with a given port out and at least 1 flag
def search_sql_port_out_with_flags(inp, cur):
    cur.execute('''SELECT flowReference, flag FROM flows
    INNER JOIN connection on flows.flowNum = connection.flowNum
    INNER JOIN flags on flags.flagNum = connection.flagNum
    where portOut = ? ORDER BY timest''', (inp,))
    return cur.fetchall()


# allows generalized queries on database
def search_sql(inp,cur):
    cur.execute(inp)
    return cur.fetchall()


def getcur():
    conn = sqlite3.connect('packets.db')
    return conn.cursor()


def print_sql_datbase():
    conn = sqlite3.connect('packets.db')
    cur = conn.cursor()
    # flow='testDB.csv'
    # addpacket(flow,conn,sql)
    flows = search_sql('SELECT * FROM flows', cur)
    relationships = search_sql('SELECT * FROM connection', cur)
    flags = search_sql('SELECT * FROM flags', cur)
    with open('flows.csv', 'w+') as flows:
        writer = csv.writer(flows)
        writer.writerows(flows)
    with open('relationships.csv', 'w+') as relationships:
        writer = csv.writer(relationships)
        writer.writerows(relationships)
    with open('flags.csv', 'w+') as flags:
        writer = csv.writer(flags)
        writer.writerows(flags)
