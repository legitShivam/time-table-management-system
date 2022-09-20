import sqlite3
import csv
import random
import os
from termcolor import colored
from tabulate import tabulate

con = sqlite3.connect('database.db')
cur = con.cursor()


def swapTimeTablePeriod(tableName, period1, period2):
    ''''
    This function swaps the period(column) in sql table
    tableName: ttId without 'TT'
    '''
    try:
        with con:
            cur.execute(f"""
            UPDATE '{tableName}' SET [P{period1}] = [P{period2}], [P{period2}] = [P{period1}]
            """)
        ques = colored(
            f"  ※ Period {period1} has been swapped with Period {period2} successfully. ", 'cyan')
        print(ques)
    except:
        ques = colored(
            f"  ※ Incorrect Time Table id or incorrect Period no.! ", 'red', attrs=('bold',))
        print(ques)


def swapTimeTableDay(tableName, day1, day2):
    '''
    This function swaps the schedule of day1 with day2 and vice-versa
    tableName: ttId without 'TT'
    '''
    try:
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
        daysFulName = ['Monday', 'Tuesday', 'Wednesday',
                       'Thursday', 'Friday', 'Saturday']
        with con:
            cur.execute(f"""
            SELECT * FROM '{tableName}'
            """)
            day1Index = days.index(day1)
            day2Index = days.index(day2)
            content = cur.fetchall()
            content[day1Index], content[day2Index] = content[day2Index], content[day1Index]

            cur.execute(f"DELETE FROM '{tableName}'")

            for shedule in content:
                cur.execute(f"""
                INSERT INTO '{tableName}' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, shedule)

            cur.execute(f"""
            UPDATE '{tableName}' SET day = 'day1' WHERE day = '{daysFulName[day1Index]}'
            """)

            cur.execute(f"""
            UPDATE '{tableName}' SET day = '{daysFulName[day1Index]}' WHERE day LIKE '{daysFulName[day2Index]}'
            """)

            cur.execute(f"""
            UPDATE '{tableName}' SET day = '{daysFulName[day2Index]}' WHERE day = 'day1'
            """)

        day1 = daysFulName[day1Index]
        day2 = daysFulName[day2Index]

        ques = colored(
            f"  ※ Schedule of {day1} has been swapped with Schedule of {day2} successfully. ", 'cyan')
        print(ques)
    except:
        ques = colored(
            f"  ※ Incorrect Time Table id or incorrect day name! ", 'red', attrs=('bold',))
        print(ques)


def editTimeTableMaually(tableName):
    try:
        cur.execute(f"""
        SELECT * FROM '{tableName}'
        """)
        content = cur.fetchall()
        fileName = f'TT{random.randint(100, 999)}.csv'
        with open(fileName, 'w') as f:
            row = csv.writer(f)
            row.writerow(['Day', 1, 2, 3, 4, 5, 6, 7, 8])

            for schedule in content:
                row.writerow(schedule)
        ques = colored(
            '  ※ Wait the CSV file is opening in M.S Excel...', 'cyan')
        print(ques)
        os.system('start ' + fileName)

        ques = colored(
            '  ※ Have you entered the data in CSV file y/n?\n  -->', 'yellow')
        ques = input(ques)
        if ques.lower() == 'y':
            with open(fileName, 'r') as f:
                reader = csv.DictReader(f)
                queryList = []
                for row in reader:
                    row = dict(row)
                    row = {key: value for key,
                           value in row.items() if value is not ''}
                    if row != {}:
                        queryList.append(dict(row))

            # This clears the existing table in sql for overiding
            cur.execute(f"DELETE FROM '{tableName}'")

            for query in queryList:
                with con:
                    cur.execute(f"""
                    INSERT INTO '{tableName}' VALUES(
                        :Day, :1, :2, :3, :4, :5, :6, :7, :8
                    )
                    """, query)
            ques = colored(
                f'  ※ Your Time Table has been edited succesfully. ', 'cyan')
            print(ques)
        else:
            editTimeTableMaually(tableName)
        try:
            os.remove(fileName)
        except:
            pass
    except:
        ques = colored(f'  ※ Theres no Time Table with id TT{tableName}', 'cyan')
        print(ques)
