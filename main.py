from termcolor import colored   # To colorise the print statement
from ddl_functions import *
from dml_functions import *
from drl_functions import *

# Estabilishing connection with the SQL Database file.
con = sqlite3.connect('database.db')
# Creating cursor to execute SQL queries.
cur = con.cursor()


def menu():
    '''
    Function: Menu
    This function displays the interactive menu to the end user

    '''
    while True:
        title = colored('TIME TABLE MANAGEMENT:', 'green',
                        attrs=('bold', 'underline'))
        print(f"""\n\t\t\t\t    {title}\n
  1)Add Time Table               5)Swap Periods Schedule        8)Read whole Time Table
  2)Remove Time Table            6)Swap Days Schedule           9)Read Time Table for a day
  3)Export TT into CSV file      7)Edit Time Table Manually     10)Get details about Time Table
  4)Exit""")

        try:
            choice = int(input('  -->'))
        except:
            choice = -1

        if choice == 1:
            title = colored('ADD TIME TABLE:', 'green',
                            attrs=('bold', 'underline'))
            print(f"""\n\t\t\t\t       {title}\n
  1)Add Teacher's Time Table 
  2)Add Class's Time Table
  3)Back
  4)Exit""")

            try:
                choice = int(input('  -->'))
            except:
                choice = -1

            if choice == 1:
                ttType = 'TT'
                ttTypeName = 'Teachers'
            elif choice == 2:
                ttType = 'CTT'
                ttTypeName = "Class's"

            elif choice == 3:
                menu()  # This will enable user to go back to main menu
            elif choice == 4:
                break
            else:
                # This will run the program again after a wrong choice
                ques = colored(
                    f'  ※ Wrong choice please try again!', 'red', attrs=('bold',))
                print(ques)
                menu()
            title = colored(f"ADD {ttTypeName} TIME TABLE:", 'green',
                            attrs=('bold', 'underline'))
            print(f"""\n\t\t\t\t   {title}\n
  1)Add Time Table via dictionay
  2)Add Time Table via CSV file
  3)Add Time Table Manually
  4)Back
  5)Exit""")
            try:
                choice = int(input('  -->'))
            except:
                choice = -1

            if choice == 1:
                ques = colored(
                    '  ※ For whom this Time Table is for?\n  -->', 'yellow')
                name = input(ques)
                ques = colored('  ※ Enter dictionary:\n  -->', 'yellow')
                # This will store the dictionary given by the user
                try:
                    dataDictionary = eval(input(ques))
                except:
                    ques = colored('  ※ Incorrect Dictionary!', 'cyan')
                    print(ques)
                # This will add the shedule(from dict form) to the sql table
                addRecordViaDict(name, dataDictionary, ttType)

            elif choice == 2:
                ques = colored(
                    '  ※ For whom this Time Table is for?\n  -->', 'yellow')
                name = input(ques)  # name of the owner of Time Table
                ques = colored('  ※ Enter file path:\n  -->', 'yellow')
                filePath = input(ques)  # stores the filepath of the CSV file
                filePath = r'{}'.format(filePath)
                # Adds the schedule(from csv form) to sql table
                addRecordViaCSV(name, filePath, ttType)
            elif choice == 3:
                ques = colored(
                    '  ※ For whom this Time Table is for?\n  -->', 'yellow')
                name = input(ques)  # name of the owner of Time Table
                # Adds schedule(from manually written into csv file) into sql table
                addRecordManualy(name, ttType)
            elif choice == 4:
                menu()  # This will enable user to go back to main menu
            elif choice == 5:
                break   # This will exit the program
            else:
                # This will run the program again after a wrong choice
                ques = colored(
                    f'  ※ Wrong choice please try again!', 'red', attrs=('bold',))
                print(ques)
                menu()
        elif choice == 2:   # Remove Time Table
            ques = colored('  ※ Enter the Time Table id?\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()
            deleteTable(ttId)

        elif choice == 3:
            ques = colored('  ※ Enter Time Table id.\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()

            exportTimeTableToCsv(ttId)

        elif choice == 4:
            break   # This will exit the program

        elif choice == 5:
            ques = colored('  ※ Enter Time Table id.\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()
            ques = colored(
                '  ※ Which Period do you want to swap from?\n  -->', 'yellow')
            period1 = input(ques)   # stores the value of period to swap from
            ques = colored(
                '  ※ Which Period do you want to swap to?\n  -->', 'yellow')
            period2 = input(ques)   # stores the value of period to swap to.
            # This will swap the swap the period1 with period2
            swapTimeTablePeriod(ttId, period1, period2)

        elif choice == 6:
            ques = colored('  ※ Enter Time Table id.\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()
            ques = colored(
                '  ※ Enter the Day which you want to swap from(like - mon...)?\n  -->', 'yellow')
            day1 = input(ques)   # stores the value of period to swap from
            ques = colored(
                '  ※ Which Period which you want to swap to(like - tue...)\n  -->', 'yellow')
            day2 = input(ques)   # stores the value of period to swap to.
            # This will swap the swap the period1 with period2
            swapTimeTableDay(ttId, day1, day2)

        elif choice == 7:
            ques = colored('  ※ Enter Time Table id.\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()
            editTimeTableMaually(ttId)

        elif choice == 8:
            ques = colored('  ※ Enter the Time Table id?\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()
            # This will read the table of the owner and print it on the screen
            readTimeTable(ttId)

        elif choice == 9:
            ques = colored('  ※ Enter Time Table id.\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()
            ques = colored(
                '  ※ Enter the Day which you want read schedule of(like - mon...)?\n  -->', 'yellow')
            day = input(ques)   # stores the value of period to swap from
            readTimeTablePerDay(ttId, day)

        elif choice == 10:
            ques = colored('  ※ Enter Time Table id.\n  -->', 'yellow')
            # name of the owner of Time Table
            ttId = input(ques).upper().replace('TT', '').strip()
            getDetails(ttId)

        else:
            # This will run the program again after a wrong choice
            ques = colored(f'  ※ Wrong choice please try again!',
                           'red', attrs=('bold',))
            print(ques)
            menu()


try:
    init()
    menu()
except:
    ques = colored(f'  ※ Something went wrong!',
                   'red', attrs=('bold',))
    print(ques)
    menu()
con.close()
