# 📦 Inventory Management & Analytics Dashboard  
A clean, professional Python + SQLite inventory system with advanced analytics, forecasting, and visualization tools. Designed for real-world inventory workflows and portfolio-quality presentation.

---

## ⭐ Overview  
This project is a complete inventory management dashboard featuring:

- Full CRUD operations  
- Daily snapshot tracking  
- Advanced analytics  
- Forecasting & trend modeling  
- ABC & Pareto analysis  
- Stockout risk prediction  
- Multiple charts & visualizations  
- Excel export  
- Organized CLI dashboard  

Everything is built in pure Python with SQLite for storage and Matplotlib for charts.

---

## 🗂️ Project Structure

    inventory/
    │
    ├── dashboard.py        # Main dashboard, analytics, charts
    ├── database.py         # SQLite CRUD operations
    ├── inventory.db        # Product database
    ├── snapshots.db        # Daily snapshot history
    └── README.md           # Project documentation

---

## 📦 Inventory Features

### Core Management
- Add products  
- Update products  
- Delete products  
- View products  
- Track categories  
- Track suppliers  
- Track price & quantity  

### Database
- SQLite backend  
- Persistent product storage  
- Daily snapshot database  

---

## 📅 Daily Snapshot System
- Automatically saves daily inventory value  
- Prevents duplicate snapshots  
- Stores historical trend data  
- Supports manual or auto snapshot  

---

## 📊 Analytics Engine

### General Analytics
- Total inventory value  
- Total product count  
- Low stock count  
- Inventory value by category  
- Inventory value by supplier  
- Top 5 products  

### Trend & Forecasting
- Trend line analysis  
- Moving average smoothing  
- Linear regression forecast  
- Confidence interval forecast  
- Combined forecast chart  
- Export forecast data to Excel  

---

## 🔍 Advanced Inventory Analytics

### ABC Analysis
Classifies products into:
- A – High-value, top contributors  
- B – Medium-value  
- C – Low-value, bulk items  

### Pareto Analysis (80/20 Rule)
Identifies the top 20% of products that generate 80% of total inventory value.

### Stockout Risk Prediction
Calculates:
- Daily usage  
- Days until stockout  
- Risk level (HIGH / MEDIUM / LOW)  

---

## 📈 Charts & Visualizations

- Category value chart  
- Supplier value chart  
- Top 5 products chart  
- Inventory trend chart  
- Moving average chart  
- Forecast chart  
- Confidence interval chart  
- Combined forecast chart  
- ABC analysis chart  
- Pareto chart  
- Stockout risk chart  

All charts are generated using Matplotlib.

---

## 🔧 Installation

### 1. Clone the repository
    git clone <your-repo-url>

### 2. Install dependencies
    pip install matplotlib openpyxl

### 3. Run the dashboard
    python dashboard.py

---

## 🚀 Why This Project Matters
This project demonstrates real inventory concepts used in:

- Retail  
- Warehousing  
- Merchandising  
- Supply chain  
- Operations analytics  

It’s perfect for:

- Portfolio projects  
- Resume enhancement  
- Python + SQL learning  
- Data analytics practice  

---

## 👨‍💻 About the Developer

**Developer:** Nick  
**Location:** Wisconsin, USA  
**Role:** Aspiring Data Analyst  
**Interests:** Python, SQL, data analytics, inventory systems, forecasting, and building real-world tools that solve practical problems.

Nick is passionate about learning through hands-on projects and building tools that reflect real business workflows. This inventory management system showcases his dedication to improving his skills in Python, SQL, analytics, and data visualization — while creating something functional, organized, and professional.

### 🛠️ Skills
- Python  
- SQL (SQLite)  
- Data Analytics  
- Forecasting & Trend Modeling  
- Matplotlib Visualization  
- Inventory Management Concepts  
- Problem Solving  
- Building CLI Tools  
- Excel Data Export  
- Regression & Confidence Intervals  

---

## 📌 Future Improvements (Optional)
- Reorder point calculator  
- Safety stock calculator  
- Inventory heatmap  
- Seasonal decomposition  
- GUI version (Tkinter / PyQt)  
- Chart export to PNG  

---

## 🏁 Final Notes
This project is fully functional and complete.  
All analytics tools, charts, and database features are implemented and tested.

Clean. Organized. Professional.


