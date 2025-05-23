import calendar
import sqlite3                  # Importing the necessary libraries
import tkinter as tk
from datetime import date
from tkinter import ttk
# from tkinter import PhotoImage
# from PIL import Image, ImageTk

import pandas as pd
from pandastable import Table

conn = sqlite3.connect('MKU_digital_assignment.db')     #This code connects to the database
cursor = conn.cursor()


# ------------------------------------------SQL Commands for category---------------------------------------------------
def update_category(category_name, category_budget): #Simple command to update categories budget
    cursor.execute(
        f"Update Category set CategoryBudget = {category_budget} where CategoryName = '{category_name}'")
    conn.commit()


def change_category(old_cat, new_cat):  #Keeping this in, but seems no longer necessary as removal of category was added
    cursor.execute(f"Update Category set CategoryName = '{new_cat}' where CategoryName = '{old_cat}'")
    conn.commit()


# -----------------------------------------SQL Commands for Spending----------------------------------------------------

def add_transaction(CategoryName, Amount):  # Function to add a new transaction
    if "{" and "}" in CategoryName:         # New categories added have {} in to highlight new added categories and this is code to take them out
        CategoryName = CategoryName.strip("{").strip("}")
    date_now = date.today()
    cursor.execute(f"Insert into Spending (CategoryID, Amount, Date) VALUES ((Select CategoryID from Category where CategoryName = '{CategoryName}'),'{Amount}','{date_now}')")
    conn.commit()

def remove_transaction(ID):
    cursor.execute(f"Delete from Spending where TransactionID = {ID}")
    conn.commit()


def update_transaction(ID, Category, Spent, Date):
    try:
        ID = int(ID)            # Quick check to ensure correct value types being added
        Spent = float(Spent)
    except:
        print("Invalid value")
    else:
        cursor.execute(
            f"Update Spending Set CategoryID = (SELECT CategoryID from Category where CategoryName = '{Category}'), Amount = {Spent}, Date = '{Date}' where TransactionID = {ID}")
        conn.commit()
        print("Success")


def monthly_return(Date): # This is the SQL code to return the monthly dashboard
    if Date == "*": #Returning the latest transactions, for the categories topic where they are per category rather than per month
        cursor.execute(f'''Select t1.CategoryName, t1.CategoryBudget, t2.Amount, t2.TransactionID,t2.Date
                from Category t1
                join Spending t2 on t1.CategoryID = t2.CategoryID''')
        return cursor.fetchall()
    elif len(Date) > 7: # Date check, it was relevant when no GUI and dates inputted manually, may not be relevant now
        Date = Date[:7] + "%"
    else:
        Date = Date + "%"
    cursor.execute(f'''Select t1.CategoryName, t1.CategoryBudget, t2.Amount, t2.TransactionID, t2.Date
        from Category t1
        join Spending t2 on t1.CategoryID = t2.CategoryID
        where Date like '{Date}' ''')
    return cursor.fetchall()


# ---------------Any Bulk major changes, hopefully smaller per transaction can be fulfilled in GUI----------------------


# -------------------------------------------------------Logic code------------------------------------------------------

def return_monthly_dashboard(Date_selected, Averages):  # Main function for returning values
    Data = monthly_return(Date_selected) #Getting the data
    match Averages:
        case 0: # This case is for the percentage bars at the top
            Spending = {
                'Category': [],
                'Budget': [],
                'Spent': []
            }
            df = pd.DataFrame(Spending)     #Creaing the panda
            Percentage_list = []
            for record in Data:  # Writing the database to panda, this one combines categories together
                if (df == record[0]).any().any():  # Checks if category already in the record
                    row_index = df.loc[df['Category'] == record[0]].index[0]
                    cell_value = df['Spent'].loc[df.index[row_index]] + record[2]               # Creating a sum of cost per category for a selected month
                    df.at[row_index, 'Spent'] = cell_value
                else:
                    New_row = [record[0], record[1], record[2]]         # if there is no matching category it will add it here
                    df.loc[len(df)] = New_row
            for row in df.itertuples():
                percentage = round(row.Spent / row.Budget * 100)            # Creates a percentage of how far through a person is with their budget
                Percentage_list.append(percentage)
            df["Percentage"] = Percentage_list
        case 1:    # This case returns the data presented in the table on the homepage
            Spending = {
                'Category': [],
                'Budget': [],
                'Spent': [],
                'Date': []
            }
            df = pd.DataFrame(Spending)
            TransactionID = []
            for record in Data:
                New_row = [record[0], record[1], record[2], record[4]]
                TransactionID.append(record[3])
                df.loc[len(df)] = New_row
            df["TransactionID"] = TransactionID
    return df


# -----------------------------------------------------------------------------------------------------------------------


class App(tk.Tk): # Decided to use Objects for each window
    def __init__(self):
        super().__init__()

        # setting up the window with a title, size of window and calling openinfunctions
        self.title('Budget Tracker')
        self.geometry('800x600')
        self.label = tk.Label(self, text='Budget Tracker')
        self.label.pack()
        self.setup_date()       # These are the main functions for setting up data
        self.start()

        self.combo_box.bind("<<ComboboxSelected>>", self.reset)
        self.combo_box_2.bind("<<ComboboxSelected>>",
                              self.reset)  # Might have to remove all widgets, then rewrite due to the buttons being local variables



    def start(self):
        self.percentage(0)
        self.add_table()        # Calls further functions
        self.add_buttons()

    def reset(self, event): # A reset window for loading a new month/refreshing data from the database
        for widget in self.winfo_children()[3:13]:      # this deletes the budget percentages section and the transaction tables
            widget.destroy()
        self.start()

    def setup_date(self):  # This will need to return an update
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        years = ["2020", "2021", "2022", "2023", "2024", "2025"]  # Gets month and year
        current_date = str(date.today())[:7].split("-")

        self.combo_box = ttk.Combobox(self, values=months, state='readonly')
        self.combo_box.set(calendar.month_name[int(current_date[1])])
        self.combo_box.place(x=5, y=50)
                                                                                    # These restrict what dates can be selected so less checks needed later and improving user experience
        self.combo_box_2 = ttk.Combobox(self, values=years, state='readonly')
        self.combo_box_2.set(current_date[0])
        self.combo_box_2.place(x=185, y=50)

    # --------------------------------------------------------------------------------------------#
    def percentage(self, event):            # Creates each section for the percentage budget, allows code to to be repeared
        data = self.return_month(True)
        data = data.sort_values(by=["Percentage"], ascending=False)
        count = 0
        xcor = 60
        for row in data.itertuples():
            if count == 5:  # Only top 5 results shown
                break
            self.create_percentage_bar(row.Category, row.Percentage, xcor, 120, count)  # Autonamte numbers
            count += 1
            xcor += 140

    def return_month(self, state): # Returning the months, getting month, adding a leading 0 if less than 10, working out with average or not
        month = str(self.combo_box.current() + 1)
        if len(month) == 1:
            month = "0" + month
        date = str(self.combo_box_2.get()) + "-" + month
        if state == True:
            data = return_monthly_dashboard(date, 0)
        else:
            data = return_monthly_dashboard(date, 1)

        return data

    def create_percentage_bar(self, category, percentage, x, y,
                              count):  # Creates the bar
        tempbar = ttk.Progressbar()
        tempbar.place(x=x, y=y)
        tempbar.step(percentage)
        tempbutton = tk.Button(self, text=category, command=lambda: self.buttonclicked(tempbutton))
        tempbutton.place(x=x, y=y + 30)

    def buttonclicked(self, buttonname):  # This can be used to bring up a categories window
        new_window = Categories(self, buttonname.cget("text"))

    def add_table(self):  # Adding in the table
        self.data = self.return_month(False)
        self.frame = tk.Frame(self)
        self.frame.place(x=0, y=300)
        edits = {
            'Category': {'type': 'readonly'},
            'Budget': {'type': 'editable', 'value': False}
        }
        self.table = Table(self.frame, dataframe=self.data, editors=edits)
        self.table.show()
        self.original = self.data.copy(deep=True)       # Getting the original data for an attempt to add a check to the data

    def add_buttons(self): # Adding in general buttons for the user such as add transction and edit category
        self.add_transaction_button = tk.Button(self, text="Add a transaction",
                                                command=lambda: self.transaction_button_clicked())
        self.add_transaction_button.place(x=600, y=300)
        self.edit_category_button = tk.Button(self, text="Edit category", command=lambda: self.edit_category_clicked())
        self.edit_category_button.place(x=600, y=350)
        self.remove_button = tk.Button(self, text="Remove transaction", command=lambda: self.remove_transaction())
        self.remove_button.place(x=600, y=400)
        self.submit_button = tk.Button(self, text="Submit changes", command=lambda: self.submit_changes())
        self.submit_button.place(x=550, y=570)

        self.reset_button = tk.Button(self,text="*", command=lambda: self.reset(0))
        self.reset_button.place(x=0, y=270)

    def transaction_button_clicked(self):
        new_window = Transaction_Widget(self)

    def edit_category_clicked(self):                        # Creating new windows
        new_window = Categories_Widget(self)

    def remove_transaction(self):
        new_window = Delete_Widget(self)

    def submit_changes(self):  # Submitting changes from updating transactions
        diff_df = self.data.compare(self.original)
        for row in self.data.itertuples():
            update_transaction(row[5],row[1],row[2],row[3],row[4])

#
class Transaction_Widget(tk.Toplevel):  # Creating a new window for transactions
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("New Window")
        self.geometry("400x300")
        self.label = tk.Label(self, text='Add new transaction')
        self.label.pack()

        cursor.execute("Select Categoryname from Category")
        categories = cursor.fetchall()
        self.Category_label = tk.Label(self, text='Enter category')
        self.Category_label.place(x=0, y=60)
        self.Category_entry = ttk.Combobox(self, values=categories, state='readonly')   #Limiting options so user can't use an unrecognised category
        self.Category_entry.place(x=100, y=60)

        self.Amount_label = tk.Label(self, text='Enter Amount')
        self.Amount_label.place(x=0, y=100)
        self.Amount_entry = tk.Entry(self)
        self.Amount_entry.place(x=100, y=100)

        self.button = tk.Button(self, text='Done', command=lambda: self.Done())
        self.button.place(x=300, y=250)

        self.focus_set()
        self.grab_set()
        self.wait_window()

    def Done(self):
        try:
            add_transaction(self.Category_entry.get(), round(float(self.Amount_entry.get())))       #Ensures correct value entered
            self.destroy()
        except ValueError:
            print("Enter a correct value")
            self.destroy()                      # Basic error handling to place errors in the terminal
        else:
            print("Error")
            self.destroy()


class Delete_Widget(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("New Window")
        self.geometry("400x300")
        self.label = tk.Label(self, text='Remove transaction')
        self.label.pack()

        self.Transaction_label = tk.Label(self, text='Enter transaction ID')
        self.Transaction_label.place(x=0, y=100)
        self.Transaction_entry = tk.Entry(self)
        self.Transaction_entry.place(x=150, y=100)

        self.button = tk.Button(self, text='Done', command=lambda: self.done())
        self.button.place(x=300, y=250)

    def done(self):
        try:
            value = int(self.Transaction_entry.get())
            remove_transaction(value)
        except:
            print("Error")
        self.destroy()




class Categories_Widget(tk.Toplevel):       # Creating a new window to edit categories
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("New Window")
        self.geometry("400x300")
        self.label = tk.Label(self, text='Edit categories')
        self.label.pack()

        cursor.execute("Select Categoryname from Category")
        categories = cursor.fetchall()
        self.Category_label = tk.Label(self, text='Enter category name')
        self.Category_label.place(x=0, y=60)
        self.Category_entry = ttk.Combobox(self, values=categories)         # This one allows editing as users need to be able to add a new category
        self.Category_entry.place(x=150, y=60)

        self.Budget_label = tk.Label(self, text='Enter category budget')
        self.Budget_label.place(x=0, y=100)
        self.Budget_entry = tk.Entry(self)
        self.Budget_entry.place(x=150, y=100)

        # self.update = ttk

        self.button = tk.Button(self, text='Done', command=lambda: self.Done())
        self.button.place(x=300, y=250)

        self.remove_button = tk.Button(self, text='Remove category', command=lambda: self.remove())
        self.remove_button.place(x=250, y=300)

        self.focus_set()
        self.grab_set()
        self.wait_window()

    def Done(self): # When done is selected
        category_name = self.Category_entry.get()
        if "{" and "}" in category_name:
            category_name = category_name.strip("{").strip("}")
        try:
            category_budget = round(float(self.Budget_entry.get()))     # error handling to ensure a number is entered
        except ValueError:
            print("Error")
        cursor.execute(f"Select CategoryID from Category where CategoryName = '{category_name}'")
        exists = cursor.fetchone()
        if exists is None:      # Check if a category exists
            try:
                cursor.execute(
                    f"INSERT into Category (CategoryName, CategoryBudget) Values ('{category_name}',{category_budget})")  # Add check to ensure no duplication
                conn.commit()
            except UnboundLocalError:   # Check is data present
                print("No data inputted")
            self.destroy()
        else:
            new_window = Error_Window(self, category_name, category_budget) # If category does exist asking if you want to replace the budget
        # ----------------------------------------

    def remove(self):   #
        category_name = self.Category_entry.get()
        cursor.execute(f"Delete from Spending where CategoryID = (Select CategoryID from Category where CategoryName = '{category_name}')")
        cursor.execute(f"Delete from Category where CategoryName = '{category_name}'")
        conn.commit()
        self.destroy()



class Error_Window(tk.Toplevel):    # error window for if a column already exists
    def __init__(self, args, name, budget):
        super().__init__(args)
        self.geometry("200x200")
        self.title("New Window")
        self.name = name
        self.budget = budget

        self.label = tk.Label(self, text='Column already exists')
        self.label_2 = tk.Label(self,
                                text='do you want to update budget?')  #
        self.label.place(x=5, y=20)
        self.label_2.place(x=5, y=40)

        self.yes = tk.Button(self, text="Yes", command=lambda: self.yes_clicked())
        self.yes.place(x=70, y=120)

        self.no = tk.Button(self, text="No", command=lambda: self.destroy())
        self.no.place(x=72, y=170)

    def yes_clicked(self):
        update_category(self.name, self.budget)
        self.destroy()  # Destroy the new window

    def no_clicked(self):           # If yes, update the table, if no don't
        self.destroy()

        self.focus_set()
        self.grab_set()
        self.wait_window()


class Categories(tk.Toplevel):      # Creates the category window, simple window just to display window
    def __init__(self, args, category):
        super().__init__(args)
        self.geometry("600x400")
        self.category = category
        print(self.category)
        data = return_monthly_dashboard("*", 1)
        data = data[data['Category'] == self.category]
        self.frame = tk.Frame(self)
        self.frame.place(x=0, y=0)
        self.table = Table(self.frame, dataframe=data)
        self.table.show()
        self.button = tk.Button(self, text="Close", command=lambda: self.destroy())
        self.button.place(x=500, y=340)


# -------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    app = App()
    app.mainloop()
