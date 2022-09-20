import sqlite3
import csv
import random
import os
from termcolor import colored
from tabulate import tabulate

con = sqlite3.connect('database.db')
cur = con.cursor()


def readTimeTable(ownerName):
    try:
        cur.execute(f"SELECT * FROM '{ownerName}'")
        content = cur.fetchall()
        heading = ('Day', 'Period 1', 'Period 2', 'Period 3',
                   'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8')
        print(tabulate(content, headers=heading))
    except:
        ques = colored('  ※ Theres no Time Table with id!', 'cyan')
        print(ques)


def readTimeTablePerDay(ownerName, day):
    try:
        cur.execute(f"SELECT * FROM '{ownerName}' WHERE day LIKE '{day}%'")
        content = cur.fetchall()
        heading = ('Day', 'Period 1', 'Period 2', 'Period 3',
                   'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8')
        print(tabulate(content, headers=heading))
    except:
        ques = colored('  ※ Theres no Time Table with id!', 'cyan')
        print(ques)


def exportTimeTableToCsv(ttId):
    try:
        cur.execute(f"""
        SELECT * FROM index_Record WHERE tableName = {ttId}
        """)
        content = cur.fetchall()
        ownerName = content[0][0]
        fileName = f'TT{content[0][1]}_{ownerName}.csv'.replace(' ', '_')

        cur.execute(f"""
        SELECT * FROM '{ttId}'
        """)
        content = cur.fetchall()
        with open(fileName, 'w') as f:
            row = csv.writer(f)
            row.writerow(['Day', 1, 2, 3, 4, 5, 6, 7, 8])

            for schedule in content:
                row.writerow(schedule)

        ques = colored(
            f'  ※ Time Table successfully exported to {fileName}\n', 'cyan')
        print(ques)

        ques = colored(
            '  ※ Wait the CSV file is opening in M.S Excel...', 'cyan')
        print(ques)
        os.system(f'start {fileName}')

    except:
        ques = colored('  ※ Theres no Time Table with id!', 'cyan')
        print(ques)


def getDetails(ttId):
    try:
        cur.execute(f"""
        SELECT tableType FROM index_Record WHERE tableName = {ttId}
        """)

        ttType = cur.fetchall()[0][0]
        if ttType == 'CTT':
            elementLabel = 'Subjects'
        else:
            elementLabel = 'Classes'

        elements = []
        for periodNo in range(1, 9):
            cur.execute(f"""
            SELECT DISTINCT P{periodNo} FROM '{ttId}'
            """)

            temp = cur.fetchall()
            for tup in temp:
                element = tup[0]
                if not element in elements:
                    elements.append(element)

        elements.sort()
        totalElements = len(elements)

        periodsInAWeek = {}
        for element in elements:
            totalPeriods = 0
            for periodNo in range(1, 9):
                cur.execute(f"""
                SELECT count(day) FROM '{ttId}' WHERE P{periodNo} = '{element}'
                """)
                totalPeriods += cur.fetchall()[0][0]
            periodsInAWeek[element] = totalPeriods

        cur.execute(f"""
        SELECT ownerName from index_Record WHERE tableName = {ttId}
        """)
        ownerName = cur.fetchall()[0][0].upper()

        field = f"""
    Time Table is for             : {ownerName}
    Time Table Type               : {ttType}
    Total number of {elementLabel}: {totalElements}
    Total number of Periods: {sum(periodsInAWeek.values())}
    """

        for element in elements:
            field = field + f"""\n  {element}
    --> Periods per week: {periodsInAWeek[element]}
    """

        title = colored(
            f"""Details of Time Table TT{ttId}""", 'green', attrs=('bold', 'underline'))

        print(f"""\n\t\t\t\t   {title}\n
        {field}""")

    except:
        ques = colored('  ※ Theres no Time Table with id!', 'cyan')
        print(ques)
