import calendar
import sqlite3
import tkinter as tk
from datetime import date
from tkinter import ttk
from time import sleep

import pandas as pd
from pandastable import Table

conn = sqlite3.connect('MKU_digital_assignment.db')
cursor = conn.cursor()


# ------------------------------------------SQL Commands for category---------------------------------------------------
def add_category(category_name, category_budget):  # Adding categories and if they exist giving the option to update
    cursor.execute(f"Select CategoryID from Category where CategoryName = '{category_name}'")
    exists = cursor.fetchone()
    if exists is None:
        cursor.execute(
            f"INSERT into Category (CategoryName, CategoryBudget) Values ('{category_name}',{category_budget})")  # Add check to ensure no duplication
        conn.commit()
    else:
        question = input("Already exists, do you want to update y/n?").lower()
        if question == "y":
            update_category(category_name, category_budget)
        else:
            print("No Query executed")


def remove_category(category_name, new_category):  # Removing categories, new category can be other
    question = input("Do you want to remove relevant transactions y/n?")
    if question == "y":
        cursor.execute(
            f"Delete from Spending where CategoryID = (Select CategoryID from Category where CategoryName = '{category_name}')")
        conn.commit()
    else:
        change_category(category_name, new_category)
    cursor.execute(f"Delete from Category where CategoryName = '{category_name}'")
    conn.commit()


def update_category(category_name, category_budget):
    cursor.execute(
        f"Update Category set CategoryBudget = {category_budget} where CategoryName = '{category_name}'")
    conn.commit()


def change_category(old_cat, new_cat):
    cursor.execute(f"Update Category set CategoryName = '{new_cat}' where CategoryName = '{old_cat}'")
    conn.commit()


# -----------------------------------------SQL Commands for Spending----------------------------------------------------

def add_transaction(CategoryName, Amount):  # Maybe need a check to ensure no null values
    if "{" and "}" in CategoryName:
        CategoryName = CategoryName.strip("{").strip("}")
    print(CategoryName, Amount)
    date_now = date.today()
    # cursor.execute(f"Insert into Spending (CategoryID, Amount, Date) VALUES ((Select CategoryID from Category where CategoryName = '{CategoryName}'),'{Amount}','{date_now}')")
    # conn.commit()


def monthly_return(Date):
    if len(Date) > 7:
        Date = Date[:7] + "%"
    else:
        Date = Date + "%"
    cursor.execute(f'''Select t1.CategoryName, t1.CategoryBudget, t2.Amount, t2.TransactionID
        from Category t1
        join Spending t2 on t1.CategoryID = t2.CategoryID
        where Date like '{Date}' ''')
    return cursor.fetchall()


# ---------------Any Bulk major changes, hopefully smaller per transaction can be fulfilled in GUI----------------------


# -------------------------------------------------------Logic code------------------------------------------------------

def return_monthly_dashboard(Date_selected, Averages):  # Check may be needed to ensure correct date format
    Spending = {
        'Category': [],
        'Budget': [],
        'Spent': []
    }
    df = pd.DataFrame(Spending)
    Data = monthly_return(Date_selected)
    match Averages:
        case True:
            Percentage_list = []
            for record in Data:  # Writing the database to panda, this one combines categories together
                if (df == record[0]).any().any():  # Checks if category already in the record
                    row_index = df.loc[df['Category'] == record[0]].index[0]
                    cell_value = df['Spent'].loc[df.index[row_index]] + record[2]
                    df.at[row_index, 'Spent'] = cell_value
                else:
                    New_row = [record[0], record[1], record[2]]
                    df.loc[len(df)] = New_row
            for row in df.itertuples():
                percentage = round(row.Spent / row.Budget * 100)
                Percentage_list.append(percentage)
            df["Percentage"] = Percentage_list
        case False:
            TransactionID = []
            for record in Data:
                New_row = [record[0], record[1], record[2]]
                TransactionID.append(record[3])
                df.loc[len(df)] = New_row
            df["TransactionID"] = TransactionID

        # Need to work out efficient way to work out percentage spent, maybe create list of percents then add to panda

    return df


# -----------------------------------------------------------------------------------------------------------------------


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Budget Tracker')
        self.geometry('800x600')
        self.label = tk.Label(self, text='Budget Tracker')
        self.label.pack()
        self.start()

        # self.combo_box.bind("<<ComboboxSelected>>", lambda: self.percentage)
        # self.combo_box_2.bind("<<ComboboxSelected>>", lambda: self.percentage)  # Might have to remove all widgets, then rewrite due to the buttons being local variables

    def start(self):
        self.setup_date()
        self.percentage()
        self.add_table()
        self.add_buttons()

    def setup_date(self):  # This will need to return an update
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        years = ["2020", "2021", "2022", "2023", "2024", "2025"]  # If I get time make it automatically update years
        current_date = str(date.today())[:7].split("-")

        self.combo_box = ttk.Combobox(self, values=months, state='readonly')
        self.combo_box.set(calendar.month_name[int(current_date[1])])
        self.combo_box.place(x=5, y=50)

        self.combo_box_2 = ttk.Combobox(self, values=years, state='readonly')
        self.combo_box_2.set(current_date[0])
        self.combo_box_2.place(x=185, y=50)

    # --------------------------------------------------------------------------------------------#
    def percentage(self):
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

    def return_month(self, state):
        month = str(self.combo_box.current() + 1)
        if len(month) == 1:
            month = "0" + month
        date = str(self.combo_box_2.get()) + "-" + month
        if state == True:
            data = return_monthly_dashboard(date, True)
        else:
            data = return_monthly_dashboard(date, False)
        return data

    def create_percentage_bar(self, category, percentage, x, y,
                              count):  # Count may be needed, as issues may arise with buttons
        tempbar = ttk.Progressbar()
        tempbar.place(x=x, y=y)
        tempbar.step(percentage)
        tempbutton = tk.Button(self, text=category, command=lambda: self.buttonclicked(tempbutton))
        tempbutton.place(x=x, y=y + 30)

    def buttonclicked(self, buttonname):  # This can be used to bring up certain categories
        print(buttonname.cget('text'))

    def add_table(self):  # Maybe add in a shop column  https://www.youtube.com/watch?v=yk9ZhoLdINo
        data = self.return_month(False)
        print(data)  # Working with panda to insert data
        self.frame = tk.Frame(self)
        self.frame.place(x=0, y=300)
        self.table = Table(self.frame, dataframe=data)
        self.table.show()

    def add_buttons(self):
        self.add_transaction_button = tk.Button(self, text="Add a transaction",
                                                command=lambda: self.transaction_button_clicked())
        self.add_transaction_button.place(x=600, y=300)
        self.edit_category_button = tk.Button(self, text="Edit category", command=lambda: self.edit_category_clicked())
        self.edit_category_button.place(x=600, y=350)

    def transaction_button_clicked(self):
        new_window = Transaction_Widget(self)

    def edit_category_clicked(self):
        new_window = Categories_Widget(self)


class Transaction_Widget(tk.Toplevel):  # Self.destory to destory widget
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
        self.Category_entry = ttk.Combobox(self, values=categories, state='readonly')
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
            add_transaction(self.Category_entry.get(), round(float(self.Amount_entry.get())))
            self.destroy()
        except ValueError:
            print("Enter a correct value")
            self.destroy()
        else:
            print("Error")
            self.destroy()


class Categories_Widget(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("New Window")
        self.geometry("400x300")
        self.label = tk.Label(self, text='Edit categories')
        self.label.pack()

        self.Category_label = tk.Label(self, text='Enter category name')
        self.Category_label.place(x=0, y=60)
        self.Category_entry = tk.Entry(self)
        self.Category_entry.place(x=150, y=60)

        self.Budget_label = tk.Label(self, text='Enter category budget')
        self.Budget_label.place(x=0, y=100)
        self.Budget_entry = tk.Entry(self)
        self.Budget_entry.place(x=150, y=100)

        self.update = ttk

        self.button = tk.Button(self, text='Done', command=lambda: self.Done())
        self.button.place(x=300, y=250)

        self.focus_set()
        self.grab_set()
        self.wait_window()

    def Done(self):  # Might have to incorporate add category to return errors
        category_name = self.Category_entry.get()
        try:
            category_budget = round(float(self.Budget_entry.get()))
        except ValueError:
            print("Error")
        cursor.execute(f"Select CategoryID from Category where CategoryName = '{category_name}'")
        exists = cursor.fetchone()
        if exists is None:
            cursor.execute(
                f"INSERT into Category (CategoryName, CategoryBudget) Values ('{category_name}',{category_budget})")  # Add check to ensure no duplication
            conn.commit()
        else:
            new_window = Error_Window(self, category_name, category_budget)
        # ----------------------------------------


class Error_Window(tk.Toplevel):
    def __init__(self, args, name, budget):
        super().__init__(args)
        self.geometry("200x200")
        self.title("New Window")
        print("ytes")
        self.name = name
        self.budget = budget

        self.label = tk.Label(self, text='Column already exists')
        self.label_2 = tk.Label(self,
                                text='do you want to update?')  # If you want, fix window size, for now this will do
        self.label.place(x=5, y=20)
        self.label_2.place(x=5, y=40)

        self.yes = tk.Button(self, text="Yes", command=lambda: self.yes_clicked())
        self.yes.place(x=70, y=120)

        self.no = tk.Button(self, text="No", command=lambda: self.destroy())
        self.no.place(x=72, y=170)

    def yes_clicked(self):
        update_category(self.name, self.budget)
        self.destroy()  # Destroy the new window


    def no_clicked(self):
        self.destroy()

        self.focus_set()
        self.grab_set()
        self.wait_window()


# -------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    app = App()
    app.mainloop()
