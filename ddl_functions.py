import sqlite3
import csv
import os
from termcolor import colored
from tabulate import tabulate
import random

con = sqlite3.connect('database.db')
cur = con.cursor()


def init():
    try:
        init.tableName = 'index_Record'
        cur.execute(f"""
        CREATE TABLE {init.tableName}(
            ownerName varchar(50),
            tableName int AUTO_INCREMENT,
            tableType varchar(50)
        )
        """)
    except:
        pass


def createTable(ownerName):
    cur.execute(f"""CREATE TABLE '{ownerName}'(
        day varchar(50),
        'P1' integer,
        'P2' integer,
        'P3' integer,
        'P4' integer,
        'P5' integer,
        'P6' integer,
        'P7' integer,
        'P8' integer)
        """)


def indexTT(ownerName, ttType):
    with con:
        cur.execute(f"""
        SELECT MAX(tableName) FROM {init.tableName}
        """)
        tableName = cur.fetchall()[0][0]
        if tableName == None:
            tableName = 0

        cur.execute(f"""
        INSERT INTO {init.tableName} VALUES(
            ?, ?, ?
        )
        """, (ownerName, tableName+1, ttType))
        return tableName+1


def addRecordViaDict(ownerName, dictionary, ttType):
    try:
        day = ['Monday', 'Tuesday', 'Wednesday',
               'Thursday', 'Friday', 'Saturday']
        queryList = []
        fieldnames = ['Day', 1, 2, 3, 4, 5, 6, 7, 8]
        for dayNo in range(0, 6):
            todaysSchedule = {'Day': day[dayNo]}
            for periodNo in range(0, 8):
                key = (dayNo, periodNo)
                if key in dictionary:
                    todaysSchedule[f'Period{periodNo + 1}'] = dictionary[key]
                else:
                    todaysSchedule[f'Period{periodNo + 1}'] = ''
            queryList.append(todaysSchedule)

        tableName = str(indexTT(ownerName, ttType))
        createTable(tableName)

        for query in queryList:
            with con:
                cur.execute(f"""
                INSERT INTO '{tableName}' VALUES(
                    :Day, :Period1, :Period2, :Period3, :Period4, :Period5, :Period6, :Period7, :Period8
                )
                """, query)

        ttId = colored(f'TT{tableName}', 'blue', attrs=('underline',))
        ques = colored(
            f'  ※ Your Time Table has been added succesfully and your Time Table id is--> ', 'cyan')
        print(ques+ttId)

        return queryList
    except:
        ques = colored('  ※ Incorrect Dictionary!', 'red', attrs=('bold',))
        print(ques)


def addRecordViaCSV(ownerName, filePath, ttType):
    try:
        with open(filePath, 'r') as f:
            reader = csv.DictReader(f)
            queryList = []
            for row in reader:
                queryList.append(dict(row))

        tableName = str(indexTT(ownerName, ttType))
        createTable(tableName)

        for query in queryList:
            with con:
                cur.execute(f"""
                INSERT INTO '{tableName}' VALUES(
                    :Day, :1, :2, :3, :4, :5, :6, :7, :8
                )
                """, query)
        ttId = colored(f'TT{tableName}', 'blue', attrs=('underline',))
        ques = colored(
            f'  ※ Your Time Table has been added succesfully and your Time Table id is--> ', 'cyan')
        print(ques+ttId)
        return queryList
    except:
        ques = colored(
            '  ※ File not found! or Invalid File format.', 'red', attrs=('bold',))
        print(ques)


def addRecordManualy(ownerName, ttType):
    fileName = f'tempTT{random.randint(100,999)}.csv'
    with open(fileName, 'w') as f:
        day = ['Monday', 'Tuesday', 'Wednesday',
               'Thursday', 'Friday', 'Saturday']
        fieldnames = ['Day', 1, 2, 3, 4, 5, 6, 7, 8]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dayNo in range(0, 6):
            todaysSchedule = {'Day': day[dayNo]}
            writer.writerow(todaysSchedule)
    ques = colored('  ※ Wait the CSV file is opening in M.S Excel...', 'cyan')
    print(ques)
    os.system('start ' + fileName)

    ques = colored(
        '  ※ Have you entered the data in CSV file y/n?\n  -->', 'yellow')
    ques = input(ques)
    if ques.lower() == 'y':
        addRecordViaCSV(ownerName, fileName, ttType)
    else:
        addRecordManualy(ownerName, ttType)

    try:
        os.remove(fileName)
    except:
        pass

    ttId = colored(f'TT{tableName}', 'blue', attrs=('underline',))
    ques = colored(
        f'  ※ Your Time Table has been added succesfully and your Time Table id is--> ', 'cyan')
    print(ques+ttId)


def deleteTable(ttId):
    try:
        cur.execute(f"DROP TABLE '{ttId}'")
        cur.execute(f"""
        DELETE FROM {init.tableName}  WHERE tableName='{ttId}'
        """)
        ques = colored(
            f'  ※ Time Table with id TT{ttId} is removed succefully.', 'cyan')
        print(ques)
    except:
        ques = colored(f"  ※ Table doesn't exits", 'cyan')
        print(ques)
