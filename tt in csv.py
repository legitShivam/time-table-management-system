# Coded By Shivam

import csv

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
                if key in data:
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


menu()
