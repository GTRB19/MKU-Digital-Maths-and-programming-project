import sqlite3
from datetime import date

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
    cursor.execute(f"Select * from Spending where Date like '{Date}'")
    print(cursor.fetchall())


# ---------------Any Bulk major changes, hopefully smaller per transaction can be fulfilled in GUI----------------------



