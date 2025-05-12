import sqlite3

conn = sqlite3.connect('MKU_digital_assignment.db')
cursor = conn.cursor()


def add_category(category_name, category_budget):
    cursor.execute(f"Select CategoryID from Category where CategoryName = '{category_name}'")
    exists = cursor.fetchone()
    if exists is None:
        cursor.execute(
            f"INSERT into Category (CategoryName, CategoryBudget) Values ('{category_name}',{category_budget})")  # Add check to ensure no duplication
        conn.commit()
    else:
        question = input("Already exists, do you want to update y/n?").lower()
        if question == "y":
            cursor.execute(
                f"Update Category set CategoryBudget = {category_budget} where CategoryName = '{category_name}'")
            conn.commit()
        else:
            print("No Query executed")


def remove_category(category_name):
    cursor.execute(f"Delete from Category where CategoryName = '{category_name}'")
    conn.commit()


add_category("Shopping", 100)
remove_category("Shopping")
