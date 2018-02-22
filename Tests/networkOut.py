def testDB():
    conn = sqlite3.connect('packets.db')
    sql = conn.cursor()
    #generateDB(sql)
    #flow='testDB.csv'
    #addPacket(flow,sql)
    test1 = searchSqlFlowsPortIn('8081', sql)
    test2 = searchSqlFlowsPortOut('35934', sql)
    test3 = searchSqlFlowsFlags('2', sql)
    test4 = searchSql('SELECT * FROM flows', sql)
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
