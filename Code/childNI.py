# handles traffic coming in from the rest of the network
'''
 NAME: Child Network In
 FILE: ConstVig/Code/ChildNI.py
 CLASSES: N/A
 EXCEPTIONS:
 FUNCTIONS:
     main
     generate_db
     add_packet
     search_sql_flows_port_in
     search_sql_flows_port_out
     search_sql
     getcur
     print_sql_database
'''
import os
import time
import csv
import sqlite3

import utilities
import pcaphandler

def main():
    s = time.time()
    cwd = os.getcwd()

    config = utilities.parse_config('NetworkIn')
    pcap_dir = config['pcapfolder']
    regex = config['regex']
    length = config['length']

    regex = regex.format(length)
    pcaphandler.split(pcap_dir)
    # Pcaps in put pcaps here should be moved or deleted
    # Will start with moved
    # if there is more than one file, move it to processed
    # only moves files
    for directory in os.listdir(pcap_dir):
        if not directory == 'processed' and os.path.isdir(pcap_dir+'\\'+directory):
            os.mkdir(pcap_dir+'\\processed\\'+directory)
            pcaphandler.get_sql_data(regex, directory, pcap_dir)
    os.chdir(cwd)
    if 'packets.db' not in os.listdir(cwd):
        conn = sqlite3.connect('packets.db')
        generate_db(conn)
    os.chdir(pcap_dir)
    for directory in os.listdir(os.getcwd()):
        if not directory == 'processed' and os.path.isdir(os.getcwd()+'\\'+directory):
            os.chdir(directory)
            add_packet(directory+'.csv', cwd)
            os.rename(pcap_dir+'\\'+directory+'\\'+directory+'.csv', pcap_dir +'\\processed\\'+directory+'\\'+directory+'.csv')
            os.chdir(pcap_dir)
            os.rmdir(directory)
    print_sql_database(cwd)
    e = time.time()
    print('Total time: ', e-s)
    return 'Analyzer is complete'

def generate_db(conn):
    conn.execute('''CREATE TABLE flows
             (id integer primary key UNIQUE,
              timest text not NULL,
              srcIP text not NULL,
              dstIP text not NULL,
              portIn integer,
              portOut integer,
              flag text not NULL,
              flowReference text not NULL)''')
    conn.commit()

def add_packet(flow, cwd):
    with open(flow, 'r') as flo:
        lines = flo.readlines()
    os.chdir(cwd)
    conn = sqlite3.connect('packets.db')
    cur = conn.cursor()
    for i in lines:
        fields = i.strip().split(',')
        cur.execute('''INSERT INTO flows(timest,srcIP,dstIP,portIn,portOut,flag,flowReference) VALUES (?,?,?,?,?,?,?)''',
                    fields)
        #(fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6]))
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


def print_sql_database(cwd):
    os.chdir(cwd)
    conn = sqlite3.connect('packets.db')
    cur = conn.cursor()
    #These were used to recreate the database
    # flow='testDB.csv'
    # addpacket(flow,conn,sql)
    flows = search_sql('''SELECT * FROM flows''', cur)
    with open('flows.csv', 'w+', newline='') as fCSV:
        writer = csv.writer(fCSV)
        writer.writerows(flows)
