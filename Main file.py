import sqlite3
from datetime import date

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
    Date = Date[:7] + "%"
    print(Date)
    cursor.execute(f'''Select t1.CategoryName, t1.CategoryBudget, t2.Amount
        from Category t1
        join Spending t2 on t1.CategoryID = t2.CategoryID
        where Date like '{Date}' ''')
    return cursor.fetchall()


# ---------------Any Bulk major changes, hopefully smaller per transaction can be fulfilled in GUI----------------------


# -------------------------------------------------------Logic code------------------------------------------------------

def return_monthly_dashboard(Date_selected):
    Spending = {
        'Category': [],
        'Budget': [],
        'Spent': []
    }
    df = pd.DataFrame(Spending)
    Data = monthly_return(Date_selected)

    for record in Data: # Writing the database to panda
        print(record[0])
        if (df == record[0]).any().any():  # Checks if category already in the record
            row_index = df.loc[df['Category'] == record[0]].index[0]
            cell_value = df['Spent'].loc[df.index[row_index]] + record[2]
            df.at[row_index, 'Spent'] = cell_value
        else:
            New_row = [record[0], record[1], record[2]]
            df.loc[len(df)] = New_row
    print(df)

    # Need to work out efficient way to work out percentage spent, maybe create list of percents then add to panda
    df["Percentage"] = [1]

    print(df)


return_monthly_dashboard("2025-05")
