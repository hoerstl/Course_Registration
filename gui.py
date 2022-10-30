import tkinter as tk
import keyboard
from tkinter import ttk
from tkinter import messagebox


class Mainwindow:
    def __init__(self, courselist):
        self.courselist = courselist
        self.root = tk.Tk()
        self.readyRoot()  # Configures the root window
        self.tabControl = ttk.Notebook(self.root)
        # Used for the Edit/Delete Tab
        self.tab1 = ttk.Frame(self.tabControl)
        # Used for the Go Time tab!
        self.tab2 = ttk.Frame(self.tabControl)
        self.readytabControl()
        # The buttons
        self.button1 = tk.Button(self.tab1, text="Edit")
        self.button2 = tk.Button(self.tab1, text="Clear")
        self.button3 = tk.Button(self.tab1, text="Name")
        self.readyViewButtons()
        # The Scrollbar/Notebook combo
        self.scrollbar = tk.Scrollbar(self.tab1)
        self.scrollbox = tk.Listbox(self.tab1)
        self.tab1pad = 50
        self.readyscrollBoxBar()

        # The Edit Frame (for when you press the edit button)
        self.editFrame = tk.Frame(self.tab1)
        self.buttonhelp = tk.Button(self.editFrame, text="?")  # This button is different because it lives in editFrame.
        self.editingcourselist = courselist.copy()  # This list serves as the course list for editing purposes.
        self.editrows = []  # This list will hold the three widgets and an indentation value for each row in the editFrame
        self.readyEditFrame()  # This creates the widgets that go inside of self.editFrame and grids them there
        self.buttonsave = tk.Button(self.tab1, text="Save")
        self.buttoncancel = tk.Button(self.tab1, text="Cancel")
        self.readyEditButtons()



        # Start the program in view mode
        self.viewMode()


    def readyRoot(self):
        """
        A short function that configures the settings for the root window.
        :return: None
        """
        self.root.title("Awesome Registering GUI")
        self.root.columnconfigure(0, weight=1)
        self.root.geometry("+700+200")


    def readytabControl(self):
        """
        Simple function that adds tab1 and tab2 to the tabControl (Notebook) widget.
        :return: None
        """
        self.tabControl.add(self.tab1, text="View/Edit")
        self.tabControl.add(self.tab2, text="Go Time!")
        self.tabControl.grid(row=0, column=1, columnspan=1, sticky="ew", padx=10)


    def readyscrollBoxBar(self):
        """
        A simple function that configures the scrollbar and scrollbox (Notebook) in self.
        :param externalpadlist: An integer that denote how much external padding to put on the left of the scrollbox
        and on the right of the scrollbar.
        :return: None
        """

        # Find the longest entry in the course list
        longest = 20
        for course in self.courselist:
            # If it's indented, judge its length based off of the indent as well
            if course[2] == 1:
                if len(course[0]) + 2 > longest:
                    longest = len(course[0]) + 2
            # Otherwise, just judge its length as is
            else:
                if len(course[0]) > longest:
                    longest = len(course[0])


        # Configure and grid self.scrollbar with set options
        self.scrollbar.config(width=20,
                              command=self.scrollbox.yview)

        # Configure and grid self.scrollbox with set options
        self.scrollbox.config(height=10,
                              width=longest,
                              yscrollcommand=self.scrollbar.set,
                              font=("Times New Roman", "15")
                              )
        self.listCourses()


    def readyViewButtons(self):
        """
        A simple function that configures button1, button2, and button3 in self.
        :return: None
        """
        self.button1.config(font=("Times New Roman", "10"), command=self.editButton)

        self.button2.config(font=("Times New Roman", "10"), command=self.clearButton)

        self.button3.config(font=("Times New Roman", "10"),
                            command=self.button3State)


    def readyEditButtons(self):
        """
        Simple function that configures the edit buttons.
        :return: None
        """
        self.buttonsave.config(command=self.saveEditButton)
        self.buttoncancel.config(command=self.cancelEditButton)
        self.buttonhelp.config(command=self.helpEditButton)


    def readyEditFrame(self):
        """
        This function configures the editing tab and gets it ready to display (DOES NOT GRID TO SCREEN).
        :return:
        """
        self.buttonhelp.grid(row=0, column=0, padx=10)
        tk.Label(self.editFrame, text="Name", fg="blue").grid(row=0, column=1)
        tk.Label(self.editFrame, text="CRN", fg="green").grid(row=0, column=2)
        self.refreshEditingFrame(True)


    def refreshEditingFrame(self, firsttime=False):
        """
        This function updates self.editing course list, delets all entry widgets, makes them all brand new, and then
        updates their labels.
        :return:
        """
        # Update the course list based on changes to the entry widgets
        if not firsttime:
            self.updateEditingCourseList()
        # Delete all current entry widgets
        self.purgeEditRows()
        # Make brand new entry widgets
        for row in range(len(self.editingcourselist)):
            # Make a blank row with the offset and lable befitting of that course and grid them to the frame
            self.makeEditingRow(row+1, self.editingcourselist[row][2])
            # Add the current classname and CRN into the entry widgets
            self.editrows[row][1].insert(0, self.editingcourselist[row][0])
            self.editrows[row][2].insert(0, self.editingcourselist[row][1])
        # Update the row labels
        self.updateEditRowLabels()


    def purgeEditRows(self):
        """
        Deletes all the widgets that were used in the editing page
        :return: None
        """
        for rownum in range(len(self.editrows)):
            self.editrows[0][0].destroy()
            self.editrows[0][1].destroy()
            self.editrows[0][2].destroy()
            self.editrows.pop(0)


    def updateEditingCourseList(self):
        """
        This function changes the entrys in self.editrows to reflect the current entries present in the self.editrows
        elements.
        :return: None
        """
        self.editingcourselist = []
        for rownum in range(len(self.editrows)):
            self.editingcourselist.append(["", "", ""])
            self.editingcourselist[rownum][0] = self.editrows[rownum][1].get()
            self.editingcourselist[rownum][1] = self.editrows[rownum][2].get()
            self.editingcourselist[rownum][2] = self.editrows[rownum][3]


    def makeEditingRow(self, rownum, offset=0):
        """
        This function makes a blank row inside self.editFrame and grids it there. It also appends the list of the
        three widgets to self.editrows.
        :param offset: This is a 1 or 0 offsets the column of the widgets
        :param rownum: This takes in an integer which decides what row to put the blank row on
        :return: None
        """

        courserow = [
            tk.Label(self.editFrame, text="To be Updated"),
            tk.Entry(self.editFrame, fg="blue"),
            tk.Entry(self.editFrame, fg="green"),
            offset
        ]
        # Bind the Entry widgets to act on tab and enter
        courserow[1].bind("<Tab>", lambda function: self.indentEditRow(rownum))
        courserow[2].bind("<Tab>", lambda function: self.indentEditRow(rownum))
        courserow[1].bind("<Return>", lambda function: self.insertEditRow(rownum+1))
        courserow[2].bind("<Return>", lambda function: self.insertEditRow(rownum+1))
        # Grid each of the widgets to the self.editFrame
        courserow[0].grid(row=rownum, column=0 + offset)
        courserow[1].grid(row=rownum, column=1 + offset)
        courserow[2].grid(row=rownum, column=2 + offset)

        self.editrows.insert(rownum-1, courserow)


    def indentEditRow(self, rownum):

        print(f"I'm indenting row {rownum}. It has an indentation of {self.editrows[rownum-1][3]}")

        if keyboard.is_pressed("Shift"):
            self.editrows[rownum-1][3] = 0
        else:
            self.editrows[rownum-1][3] = 1

        self.refreshEditingFrame()

        """
        self.editrows[rownum-1][0].grid_remove()
        self.editrows[rownum-1][1].grid_remove()
        self.editrows[rownum-1][2].grid_remove()

        if keyboard.is_pressed("Shift"):  # For some reason, this line of code doesn't give true unless called twice.
            self.editrows[rownum-1][3] = 0
        else:
            self.editrows[rownum-1][3] = 1

        self.editrows[rownum-1][0].grid(row=rownum, column=0 + self.editrows[rownum-1][3])
        self.editrows[rownum-1][1].grid(row=rownum, column=1 + self.editrows[rownum-1][3])
        self.editrows[rownum-1][2].grid(row=rownum, column=2 + self.editrows[rownum-1][3])

        self.updateEditRowLabels()
        """


    def updateEditRowLabels(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        bignumber = 0
        smallletter = 0
        for row in self.editrows:
            # Decide what label to give each row
            if row[3] == 0:
                bignumber += 1
                first = str(bignumber)
                second = ""
                smallletter = 0
            else:
                first = str(bignumber)
                second = alphabet[smallletter]
                if smallletter < 25:
                    smallletter += 1

            row[0].config(text=first + second + ". ")


    def insertEditRow(self, rownum):
        """
        This function inserts a blank row at the given index and regrids all the entry rows.
        :return: None
        """

        self.makeEditingRow(rownum, self.editingcourselist[rownum-2][2])

        self.refreshEditingFrame()


    def button3State(self):
        """
        Changes the name of self.button3 to CRN if it was Name, and Name if it was CRN. It then updates the scrollbox.
        :return: None
        """
        if self.button3["text"] == "Name":
            self.button3["text"] = "CRN"
        elif self.button3["text"] == "CRN":
            self.button3["text"] = "Name"

        self.listCourses()


    # Still need to implement this
    def saveEditButton(self):
        """
        Checks to see if proper edits were made. If they were it saves the edits made to self.courselist and then
        updates them everywhere. Then switches to view mode.
        :return:
        """
        valid = True
        for row in self.editrows:
            if not self.validateName(row[1].get()):
                row[1].config(bg="red")
                valid = False
            else:
                row[1].config(bg="white")
            if not self.validateCRN(row[2].get()):
                row[2].config(bg="red")
                valid = False
            else:
                row[2].config(bg="white")

        if valid:
            print("This should save everything now!")
            self.updateEditingCourseList()
            self.courselist = self.editingcourselist.copy()
            self.viewMode()
        else:
            print("One or more of the boxes had errors in it.")


    def validateName(self, name):
        """
        This function is used by the save button to validate the name entries. As of now, there is no validation process
        for the name entries so this function always returns True. This is a placeholder for future validation if
        desired.
        :param name: A string that contains the name to be checked
        :return: Boolean
        """
        return True


    def validateCRN(self, crn):
        """
        This function validates a suspect CRN and will return True if it followes the 5 number format and False if it
        does not.
        :param crn: This is the suspect CRN. It can be a string or an integer.
        :return: Boolean
        """
        valid = True
        if len(crn) != 5 or not str(crn).isnumeric():
            valid = False

        return valid


    def cancelEditButton(self):
        for row in range(len(self.courselist)):
            # Delete Current data
            self.editrows[row][1].delete(0, tk.END)
            self.editrows[row][2].delete(0, tk.END)
            # Add the known classnames and CRNs into the entry widgets
            self.editrows[row][1].insert(0, self.courselist[row][0])
            self.editrows[row][2].insert(0, self.courselist[row][1])

        self.viewMode()


    def helpEditButton(self):
        """
        This function describes the behavior of the help button on the editing screen.
        :return: None
        """
        print("I'm the help button")
        messagebox.showinfo("Help",
                            "Enter:\n" +
                            "Press the enter button to add a new class to the list.\n\n" +
                            "Tab:\n" +
                            "Press tab to indent a class and mark it as a backup for the class before it.\n\n" +
                            "Shift+Tab\n" +
                            "Press shift+tab to remove the indent and makes it afirst choice.")


    def listCourses(self):
        """
        Clears and Inserts the courses into self.scrollbox so it can update based on the state of button3.
        :return: None
        """
        # Enable the scrollbox for the duration of this function
        self.scrollbox.config(state=tk.NORMAL)

        if self.button3['text'] == "Name":
            view = 0
        else:
            view = 1

        # Clear out the scrollbox
        self.scrollbox.delete(0, tk.END)

        for course in self.courselist:
            if course[2] == 0:
                offset = ""
            else:
                offset = "--> "
            self.scrollbox.insert(tk.END, offset + str(course[view]))

        # Disable the scrollbox when you're done
        self.scrollbox.config(state=tk.DISABLED)


    def editMode(self):
        """
        This function sets up the UI to accept user input for classes
        :return: None
        """
        print("I am the edit button!")
        # Hides the parts of tab1 that are for viewing
        self.scrollbox.grid_remove()
        self.scrollbar.grid_remove()
        self.button1.grid_remove()
        self.button2.grid_remove()
        self.button3.grid_remove()


        # Grids the editing frame
        self.editFrame.grid(row=0, column=0, columnspan=4, sticky="e", padx=self.tab1pad)
        self.buttonsave.grid(row=1, column=1, sticky="", pady=30)
        self.buttoncancel.grid(row=1, column=2, sticky="", pady=30)


    def viewMode(self):
        """
        This function swaps tab1 from editing mode to viewing mode
        :return: None
        """
        # Hides the editing widgets
        self.editFrame.grid_remove()
        self.buttonsave.grid_remove()
        self.buttoncancel.grid_remove()

        # Grids the viewing widgets
        self.button1.grid(row=1, column=1, sticky="", pady=30)
        self.button2.grid(row=1, column=2, sticky="", pady=30)
        self.button3.grid(row=1, column=3, sticky="", pady=30)
        self.scrollbar.grid(row=0, column=5, sticky="nsw", padx=(0, self.tab1pad))

        self.scrollbox.grid(row=0, column=0, columnspan=4, sticky="e", padx=(self.tab1pad, 0))


    def editButton(self):
        """
        This function describes the behavior of the edit button.
        :return: None
        """
        self.editingcourselist = self.courselist.copy()
        self.refreshEditingFrame(True)
        self.editMode()


    def clearButton(self):
        """
        This function describes the behavior of the clear button.
        :return: None
        """

        self.editingcourselist = [["", "", 0]]
        self.refreshEditingFrame()
        self.editMode()




def main():
    courselist = [
        ["Linear", 16514, 0],
        ["Calc", 16597, 1],
        ["Fundamentals", 14779, 0],
        ["Differential Equations", 11798, 1],
        ["Computer Security", 47774, 0],
        ["Networking", 77165, 0]
    ]
    root = Mainwindow(courselist)
    root.root.mainloop()


main()
