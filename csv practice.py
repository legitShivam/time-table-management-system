# Coded By Shivam

import csv


def writeCSV(fileName):
    with open(fileName, 'w') as f:
        row = csv.writer(f)
        row.writerow(['Roll_no', 'Name', 'Class', 'Section'])
        while True:
            row = csv.writer(f)
            data = input(
                "Enter student data(Roll no, Name, Class, Section), seperate column by whitespace:\n\t-->").split()
            if data == ['y'] or data == ['Y']:
                break
            else:
                row.writerow(data)


def readCSV(fileName):
    with open(fileName, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'\nRoll_no\tName\tClass\tSection')
                line_count += 1
            else:
                try:
                    print(f'{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}')
                    line_count += 1
                except:
                    line_count += 1
        print(f'Processed {line_count} lines.')


def writeTT(fileName, data):
    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    with open(fileName, 'w') as f:
        fieldnames = ['Day/Period', 1, 2, 3, 4, 5, 6, 7, 8]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dayNo in range(0, 6):
            todaysSchedule = {'Day/Period':day[dayNo]}
            for periodNo in range(0,8):
                key = (dayNo, periodNo)
                if key in dic:
                    todaysSchedule[periodNo + 1] = data[key]
                else:
                    todaysSchedule[periodNo + 1] = 'Free'
            writer.writerow(todaysSchedule)




def readTT(fileName):
    with open(fileName, 'r') as f:
        reader = csv.DictReader(f)
        print(f"Day/Period\t1\t2\t3\t4\t5\t6\t7\t8")
        for row in reader:
            output = f"{row['Day/Period']}\t"
            for key in range(1,9):
                output += (f"{row[f'{key}']}\t")
            print(output)


def menu():
    while True:
        print('\nMENU:\n  1)Write Time Table\n  2)Read Time Table\n  3)Exit')
        choice = int(input())

        if choice == 1:
            fileName = input("Enter file name:\n  -->")
            data = input("Enter dictionary:\n  -->")
            data = eval(data)
            writeTT(fileName, data)
        elif choice == 2:
            fileName = input("Enter file name:\n  -->")
            readTT(fileName)
        elif choice == 3:
            break


dic = {(0, 0): "Nikhil", (0, 1): "Akshat", (1, 2): "Akash"}
menu()


