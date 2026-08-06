# 📦 Inventory Management Database
A modular, Python‑based inventory management system designed to track products, suppliers, categories, stock levels, and generate useful reports. Built with SQLite for storage and organized into clean, maintainable modules.

---

## 🚀 Features

### Product Management
- Add, edit, delete products
- Restock or reduce inventory
- Track quantity, price, category, and supplier

### Supplier Management
- Add, edit, delete suppliers
- Search suppliers by name

### Category Management
- Add, edit, delete categories
- Search categories by name

### Search Tools
- Search products by category
- Search products by supplier
- Search by price range
- Low‑stock product search
- Search by category name
- Search by inventory value

### Reports & Analytics
- Dashboard summary
- CSV export for products (new feature!)

---

## 🗂 Project Structure

Inventory Management Database/
│
├── .gitignore
├── inventory.db
├── README.md
├── token.txt
│
└── inventory/
    ├── __init__.py
    ├── main.py
    ├── db.py
    ├── utils.py
    ├── products.py
    ├── suppliers.py
    ├── categories.py
    ├── search.py
    ├── reports.py

---

## 🛠 Technologies Used
- Python 3
- SQLite (local database)
- CSV module (for export)
- Modular architecture for clean, scalable code

---

## ▶️ How to Run

1. Make sure you have Python installed
2. Open the project in VS Code or Codespaces
3. Run:

   python inventory/main.py

4. Use the menu to manage products, suppliers, categories, search, and reports

---

## 📤 CSV Export

You can export all products to a CSV file using:

Reports → Export Products to CSV

This generates:

products_export.csv

in your project root.

---

## 📌 Future Improvements
- Export suppliers and categories to CSV
- Add user login roles
- Add inventory value charts
- Add automatic low‑stock notifications
- Add JSON or Excel export options
- Add a GUI or web interface

---

## 👤 Author
**Nick**
Aspiring Data Analyst & Python Developer  
Building practical tools and learning through hands‑on projects.
