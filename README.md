# Inventory Management Database

A complete SQL + Python inventory management system designed to support practical data skills including database management (CRUD operations), relational data modeling, and backend workflow logic. This project demonstrates how to design structured data systems, maintain data integrity, and build scalable backend components for real-world inventory operations.

---

## 📦 Project Overview

This system manages core inventory operations:

- Product registration with unique identifiers  
- Supplier tracking and relationships  
- Stock updates and quantity management  
- Timestamp logging for all database changes  
- SQL queries for reporting, insights, and workflow automation  

The project is intentionally modular, allowing future expansion into analytics, dashboards, and API-driven workflows.

---

## 🧠 Skills Demonstrated

- **SQL schema design** — tables, keys, constraints, relationships  
- **Database design** — normalization, workflow logic, data integrity  
- **Python backend development** — modular structure, clean separation of concerns  
- **Problem-solving** — designing conceptual workflows and control flow  
- **Version control** — Git, GitHub, SSH authentication  
- **Data engineering fundamentals** — structured data pipelines and maintainable systems  

---

## 🛠 Tech Stack

- **Python 3**
- **SQLite** (local development)
- **PostgreSQL** (optional upgrade path)
- **SQLAlchemy** (optional ORM layer)
- **Git + GitHub** (version control)

---

## 📁 Project Structure

The project is organized into a clean, modular layout that separates application logic, database operations, and documentation. This makes the system easier to maintain, extend, and scale.

inventory_management_database/
│
├── main.py
│   - The main entry point of the application.
│   - Handles user interaction, menu logic, and calls functions from the inventory package.
│
├── inventory/
│   ├── db.py
│   │   - Core database module.
│   │   - Handles SQLite connection, table creation, CRUD operations, and query logic.
│   │   - Central place for all data-access logic.
│   │
│   └── __init__.py
│       - Marks the folder as a Python package.
│       - Allows imports like: from inventory.db import connect_db
│
├── README.md
│   - Full project documentation.
│   - Includes overview, setup instructions, tech stack, skills demonstrated, and future enhancements.
│
└── (future folders planned)
    ├── analytics/
    │   - Power BI exports, SQL reporting scripts, KPI calculations.
    │
    ├── api/
    │   - REST API endpoints for external integrations.
    │
    ├── data/
    │   - CSV import/export, sample datasets, logs.
    │
    └── tests/
        - Automated tests for database logic and workflows.


## ▶️ How to Run the Project

If you want to run this project locally:

1. **Clone the repository**
2. **Navigate into the project**
3. **Run the program**
The system will guide you through adding, updating, deleting, and viewing inventory items. All changes are automatically timestamped.

---

## 🚀 Future Enhancements

- Power BI dashboards for inventory insights  
- CSV import/export for bulk operations  
- REST API design for external integrations  
- Low-stock alerts and automated notifications  
- Supplier performance analytics  
- BOM (Bill of Materials) support  
- ECN (Engineering Change Notice) workflow  
- Provisioning & stock forecasting  

---

## 👤 About the Developer

**Nick** — aspiring data analyst focused on SQL, Python, and building real-world data projects.  
This project is part of my growing portfolio demonstrating my ability to design, build, and ship data-driven systems.

---

## 📄 License

MIT License
