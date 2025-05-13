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
