# categories.py

import sqlite3


# ---------------------------------------------------------
# Add Category
# ---------------------------------------------------------
def add_category(conn):
    cur = conn.cursor()
    try:
        name = input("Category name: ")

        cur.execute("""
            INSERT INTO categories (name)
            VALUES (?)
        """, (name,))

        conn.commit()
        print("Category added successfully.")
    except Exception as e:
        print("Error adding category:", e)


# ---------------------------------------------------------
# View Categories
# ---------------------------------------------------------
def view_categories(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()

        print("\n=== Category List ===")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}")
        print()
    except Exception as e:
        print("Error viewing categories:", e)


# ---------------------------------------------------------
# Edit Category
# ---------------------------------------------------------
def edit_category(conn):
    cur = conn.cursor()
    try:
        category_id = input("Enter Category ID to edit: ")

        cur.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        category = cur.fetchone()

        if not category:
            print("Category not found.")
            return

        print(f"Current Name: {category[1]}")
        new_name = input("New name (leave blank to keep current): ") or category[1]

        cur.execute("""
            UPDATE categories
            SET name = ?
            WHERE id = ?
        """, (new_name, category_id))

        conn.commit()
        print("Category updated successfully.")

    except Exception as e:
        print("Error editing category:", e)


# ---------------------------------------------------------
# Delete Category
# ---------------------------------------------------------
def delete_category(conn):
    cur = conn.cursor()
    try:
        category_id = input("Enter Category ID to delete: ")

        cur.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        category = cur.fetchone()

        if not category:
            print("Category not found.")
            return

        confirm = input(f"Are you sure you want to delete '{category[1]}'? (y/n): ")
        if confirm.lower() != "y":
            print("Deletion cancelled.")
            return

        cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        print("Category deleted successfully.")

    except Exception as e:
        print("Error deleting category:", e)


# ---------------------------------------------------------
# Search Category
# ---------------------------------------------------------
def search_category(conn):
    cur = conn.cursor()
    try:
        keyword = input("Enter category name or keyword: ")

        cur.execute("""
            SELECT * FROM categories
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))

        rows = cur.fetchall()

        if not rows:
            print("No categories found.")
            return

        print("\n=== Search Results ===")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}")
        print()

    except Exception as e:
        print("Error searching categories:", e)


# ---------------------------------------------------------
# Choose Category (used by products.py)
# ---------------------------------------------------------
def choose_category(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM categories")
    rows = cur.fetchall()

    if not rows:
        print("No categories found. Add one first.")
        return None

    print("\n=== Choose a Category ===")
    for row in rows:
        print(f"{row[0]}. {row[1]}")

    while True:
        try:
            choice = int(input("Enter category ID: "))
            if any(row[0] == choice for row in rows):
                return choice
            else:
                print("Invalid category ID. Try again.")
        except ValueError:
            print("Please enter a valid number.")
