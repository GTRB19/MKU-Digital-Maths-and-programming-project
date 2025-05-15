import calendar
import sqlite3
import tkinter as tk
from datetime import date
from tkinter import ttk

import pandas as pd

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

def add_transaction(CategoryID, Amount):
    date_now = date.today()
    cursor.execute(f"Insert into Spending (CategoryID, Amount, Date) VALUES ('{CategoryID}','{Amount}','{date_now}')")
    conn.commit()


def monthly_return(Date):
    if len(Date) > 7:
        Date = Date[:7] + "%"
    else:
        Date = Date + "%"
    cursor.execute(f'''Select t1.CategoryName, t1.CategoryBudget, t2.Amount
        from Category t1
        join Spending t2 on t1.CategoryID = t2.CategoryID
        where Date like '{Date}' ''')
    return cursor.fetchall()


# ---------------Any Bulk major changes, hopefully smaller per transaction can be fulfilled in GUI----------------------


# -------------------------------------------------------Logic code------------------------------------------------------

def return_monthly_dashboard(Date_selected):  # Check may be needed to ensure correct date format
    Percentage_list = []
    Spending = {
        'Category': [],
        'Budget': [],
        'Spent': []
    }
    df = pd.DataFrame(Spending)
    Data = monthly_return(Date_selected)
    for record in Data:  # Writing the database to panda
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

    # Need to work out efficient way to work out percentage spent, maybe create list of percents then add to panda
    df["Percentage"] = Percentage_list
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
        self.setup_date()
        self.percentage()

        # self.combo_box.bind("<<ComboboxSelected>>", lambda: self.percentage)
        # self.combo_box_2.bind("<<ComboboxSelected>>", lambda: self.percentage)  # Might have to remove all widgets, then rewrite due to the buttons being local variables


    def start(self):
        self.setup_date()
        self.percentage()

    def setup_date(self):  # This will need to return an update
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        years = ["2020", "2021", "2022", "2023", "2024", "2025"]  # If I get time make it automatically update years
        current_date = str(date.today())[:7].split("-")
        self.combo_box = ttk.Combobox(self, values=months, )
        self.combo_box.set(calendar.month_name[int(current_date[1])])
        self.combo_box.place(x=5, y=50)
        self.combo_box_2 = ttk.Combobox(self, values=years)
        self.combo_box_2.set(current_date[0])
        self.combo_box_2.place(x=185, y=50)

#--------------------------------------------------------------------------------------------#
    def percentage(self):
        month = str(self.combo_box.current() + 1)
        if len(month) == 1:
            month = "0" + month
        date = str(self.combo_box_2.get()) + "-" + month
        data = return_monthly_dashboard(date)
        data = data.sort_values(by = ["Percentage"], ascending=False)
        print(data)
        count = 0
        xcor = 60
        for row in data.itertuples():
            if count == 5: #Only top 5 results shown
                break
            print(row.Category, row.Percentage)
            self.create_percentage_bar(row.Category,row.Percentage, xcor,  120, count) #Autonamte numbers
            count += 1
            xcor += 140

    def create_percentage_bar(self, category, percentage, x,y, count): # Count may be needed, as issues may arise with buttons
        tempbar = ttk.Progressbar()
        tempbar.place(x = x, y = y)
        tempbar.step(percentage)
        tempbutton = tk.Button(self, text = category, command=lambda: self.buttonclicked(tempbutton))
        tempbutton.place(x = x, y = y+30)

    def buttonclicked(self, buttonname): # This can be used to bring up certain categories
        print(buttonname.cget('text'))

#-------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    app = App()
    app.mainloop()
