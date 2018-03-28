# handles traffic coming in from the rest of the network

# NAME: Child Network In
# FILE: ConstVig/Code/ChildNI.py
# CLASSES: N/A
# EXCEPTIONS:
# FUNCTIONS:
#     main
#     generate_db
#     addpacket
#     search_sql_flows_port_in
#     search_sql_flows_port_out
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


def main():
    # Checks for type and returns the input,
    # otherwise returns an error message
    # Here is where database stuff begins
    config = utilities.parse_config('NetworkIn')
    regex = config['regex']
    length = config['length']

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
    flows = pcaphandler.get_sql_data(regex, length)
    for dir_name in os.listdir(pcap_dir):
        if os.path.isdir(dir_name) and not dir_name == "processed":
            os.rename(pcap_dir+'\\'+dir_name,pcap_dir+'\\processed\\'
                      +dir_name)
    flowsCSV = flows[0]
    addpacket(flowsCSV, conn, cur)
    os.chdir('C:\\Users\\T\\Documents\\GitHub\\ConstVig\\Code')
    print_sql_database()


def generate_db(conn):
    conn.execute('''CREATE TABLE flows
             (flowNum integer primary key,
              timest real,
              portIn integer,
              portOut integer,
              flowReference text)''')

def addpacket(flow, conn, cur):
    with open(flow, 'r+') as flo:
        lines = flo.readlines()
    data_groups = []
    for i in lines:
        fields = i.split(',')
        temp = (fields[0], fields[1], fields[2], fields[3])
        data_groups.append(temp)
    for line in range(0, len(data_groups)):
        cur.execute("""INSERT INTO flows(timest, portIn, portOut, flowReference) VALUES (?, ?, ?, ?)""", data_groups[line])
    conn.commit()

# finds flows with a given port in
def search_sql_flows_port_in(inp,cur):
    cur.execute('''SELECT flowReference FROM flows where portIn = ?''', (inp,))
    return cur.fetchall()


# finds flows with a given port out
def search_sql_flows_port_out(inp,cur):
    cur.execute('''SELECT flowReference FROM flows where portOut = ?''', (inp,))
    return cur.fetchall()

# allows generalized queries on database
def search_sql(inp,cur):
    cur.execute(inp)
    return cur.fetchall()


def getcur():
    conn = sqlite3.connect('packets.db')
    return conn.cursor()


def print_sql_database():
    conn = sqlite3.connect('packets.db')
    cur = conn.cursor()
    #These were used to recreate the database
    # flow='testDB.csv'
    # addpacket(flow,conn,sql)
    flows = search_sql("""SELECT * FROM flows""", cur)
    with open('flows.csv', 'w+') as fCSV:
        writer = csv.writer(fCSV)
        writer.writerows(flows)
