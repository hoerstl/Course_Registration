

import keyboard

number = 1


def type_nums(file, boo=False):
    for line in file.readlines():
        keyboard.write(line[:-1])
        if boo:
            keyboard.wait('backspace', True)
        else:
            keyboard.press("tab")


def wellbackup():
    keyboard.write("20468")


def gstrbackup1():
    keyboard.write("20202")


def gstrbackup2():
    keyboard.write("20209")

keyboard.add_hotkey("shift+w", wellbackup)
keyboard.add_hotkey("shift+g", gstrbackup1)
keyboard.add_hotkey("shift+h", gstrbackup2)


ask = input("Would you like to \"change\" your CRNs? or register \"reg\" using them?\n")
if ask.lower() == "change":
    file = open("CRNs.txt", "w+")
    ask = input("What is the CRN for course #{}?\n".format(number))
    while ask.lower() != "stop":
        if len(ask) != 5:
            print("The CRN that you input wasn't an acceptable length, check and try again.")
        else:
            number += 1
            file.write(ask+"\n")
        ask = input("What is the CRN for course #{}? (type 'stop' to stop)\n".format(number))

elif ask.lower() == "reg":
    file = open("CRNs.txt", "r")
    print("Click into the first CRN box and press the backspace key to type the previously entered numbers.")
    keyboard.wait("backspace", True)
    type_nums(file)
    keyboard.press_and_release("enter")
















elif ask.lower() == "r":
    file = open("CRNs.txt", "r")
    print("Click into the first CRN box and press the backspace key each time to type the previously entered numbers.")
    keyboard.wait("backspace", True)
    type_nums(file, True)
    keyboard.press_and_release("enter")
else:
    file = open("CRNs.txt", "r")
    print("Invalid input, please restart the program and try again.")



x = input("End program: \n")
print("done")

file.close()



