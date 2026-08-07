import sqlite3
import matplotlib.pyplot as plt
import openpyxl

from openpyxl import Workbook

DB_PATH = "inventory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# -----------------------------
#   DASHBOARD METRICS
# -----------------------------

def total_inventory_value():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(quantity * price) FROM products;")
    value = cursor.fetchone()[0]
    conn.close()
    return value if value else 0

def total_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products;")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def low_stock_count(threshold=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products WHERE quantity < ?;", (threshold,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def inventory_value_by_category():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT categories.name, SUM(products.quantity * products.price)
        FROM products
        JOIN categories ON products.category_id = categories.id
        GROUP BY categories.name;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def inventory_value_by_supplier():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT suppliers.name, SUM(products.quantity * products.price)
        FROM products
        JOIN suppliers ON products.supplier_id = suppliers.id
        GROUP BY suppliers.name;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def top_5_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, (quantity * price) AS value
        FROM products
        ORDER BY value DESC
        LIMIT 5;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def abc_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, (price * quantity) AS value
        FROM products
        ORDER BY value DESC;
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return []

    total_value = sum(row[1] for row in rows)
    cumulative = 0

    results = []

    for name, value in rows:
        cumulative += value
        percentage = (cumulative / total_value) * 100

        if percentage <= 80:
            category = "A"
        elif percentage <= 95:
            category = "B"
        else:
            category = "C"

        results.append((name, value, percentage, category))

    return results

def pareto_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, (price * quantity) AS value
        FROM products
        ORDER BY value DESC;
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return []

    total_value = sum(row[1] for row in rows)
    cumulative = 0

    results = []

    for name, value in rows:
        cumulative += value
        pct = (cumulative / total_value) * 100
        results.append((name, value, pct))

    return results

def stockout_risk(daily_usage=1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, quantity
        FROM products;
    """)

    rows = cursor.fetchall()
    conn.close()

    results = []

    for name, qty in rows:
        if daily_usage <= 0:
            days_left = None
            risk = "Unknown"
        else:
            days_left = qty / daily_usage

            if days_left < 3:
                risk = "HIGH"
            elif days_left < 7:
                risk = "MEDIUM"
            else:
                risk = "LOW"

        results.append((name, qty, daily_usage, days_left, risk))

    return results




def view_abc_analysis():
    data = abc_analysis()
    if not data:
        print("No product data available.")
        return

    print("\nABC Analysis")
    print("-" * 40)
    print(f"{'Product':20} {'Value':10} {'Cum%':10} {'Class'}")
    print("-" * 40)

    for name, value, pct, category in data:
        print(f"{name:20} ${value:<10.2f} {pct:<10.2f} {category}")

def view_pareto_analysis():
    data = pareto_analysis()
    if not data:
        print("No product data available.")
        return

    print("\nPareto Analysis (80/20 Rule)")
    print("-" * 50)
    print(f"{'Product':20} {'Value':10} {'Cum%':10}")
    print("-" * 50)

    for name, value, pct in data:
        print(f"{name:20} ${value:<10.2f} {pct:<10.2f}")

def view_stockout_risk(daily_usage=1):
    data = stockout_risk(daily_usage)
    if not data:
        print("No product data available.")
        return

    print("\nStockout Risk Prediction")
    print("-" * 60)
    print(f"{'Product':20} {'Qty':6} {'Days Left':10} {'Risk'}")
    print("-" * 60)

    for name, qty, usage, days_left, risk in data:
        days_text = f"{days_left:.1f}" if days_left is not None else "N/A"
        print(f"{name:20} {qty:<6} {days_text:<10} {risk}")






# -----------------------------
# HISTORY + SNAPSHOTS
#------------------------------

def save_daily_snapshot():
    conn = get_connection()
    cursor = conn.cursor()

    value = total_inventory_value()

    cursor.execute("""
        INSERT INTO inventory_history (snapshot_date, total_value)
        VALUES (DATE('now'), ?);
    """, (value,))

    conn.commit()
    conn.close()

    print("Daily snapshot saved.")

def get_trend_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT snapshot_date, total_value
        FROM inventory_history
        ORDER BY snapshot_date;
    """)

    results = cursor.fetchall()
    conn.close()
    return results

def snapshot_exists_today():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM inventory_history
        WHERE snapshot_date = DATE('now');
    """)

    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def auto_snapshot():
    if snapshot_exists_today():
        return  # Already saved today

    save_daily_snapshot()

def moving_average(values, window=3):
    if len(values) < window:
        return []

    ma = []
    for i in range(window - 1, len(values)):
        window_slice = values[i - window + 1:i + 1]
        ma.append(sum(window_slice) / window)

    return ma

def linear_regression_forecast(values):
    n = len(values)
    if n < 2:
        return None, None  # Not enough data

    # x = day index (0,1,2,...)
    x = list(range(n))
    y = values

    # Calculate means
    x_mean = sum(x) / n
    y_mean = sum(y) / n

    # Calculate slope (m)
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        return None, None

    m = numerator / denominator

    # Calculate intercept (b)
    b = y_mean - m * x_mean

    return m, b

def regression_variance(values, m, b):
    n = len(values)
    if n < 2:
        return None

    x = list(range(n))
    residuals = [(values[i] - (m * x[i] + b)) ** 2 for i in range(n)]
    variance = sum(residuals) / (n - 1)
    return variance




# -----------------------------
#   CHARTS
# -----------------------------

def chart_category_value():
    data = inventory_value_by_category()
    if not data:
        print("No category data available.")
        return

    names = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.bar(names, values)
    plt.title("Inventory Value by Category")
    plt.xlabel("Category")
    plt.ylabel("Value ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def chart_supplier_value():
    data = inventory_value_by_supplier()
    if not data:
        print("No supplier data available.")
        return

    names = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.pie(values, labels=names, autopct="%1.1f%%")
    plt.title("Supplier Contribution to Inventory Value")
    plt.show()

def chart_top_5_products():
    data = top_5_products()
    if not data:
        print("No product data available.")
        return

    names = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.bar(names, values, color="skyblue")
    plt.title("Top 5 Most Valuable Products")
    plt.xlabel("Product")
    plt.ylabel("Inventory Value ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def chart_inventory_trend():
    data = get_trend_data()
    if not data:
        print("No trend data available. Save a snapshot first.")
        return

    dates = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.plot(dates, values, marker='o', linestyle='-', color='green')
    plt.title("Inventory Value Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Inventory Value ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def chart_moving_average_trend(window=3):
    data = get_trend_data()
    if not data:
        print("No trend data available. Save a snapshot first.")
        return

    dates = [row[0] for row in data]
    values = [row[1] for row in data]

    ma_values = moving_average(values, window)

    if not ma_values:
        print(f"Not enough data for a {window}-day moving average.")
        return

    # Align dates with MA values
    ma_dates = dates[window - 1:]

    plt.plot(dates, values, marker='o', linestyle='-', color='gray', alpha=0.5, label="Daily Value")
    plt.plot(ma_dates, ma_values, marker='o', linestyle='-', color='blue', label=f"{window}-Day Moving Average")

    plt.title(f"Inventory Value Trend (Moving Average: {window} Days)")
    plt.xlabel("Date")
    plt.ylabel("Total Inventory Value ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def chart_forecast_line(days_ahead=7):
    data = get_trend_data()
    if not data:
        print("No trend data available.")
        return

    dates = [row[0] for row in data]
    values = [row[1] for row in data]

    m, b = linear_regression_forecast(values)
    if m is None:
        print("Not enough data for forecasting.")
        return

    # Create forecast points
    n = len(values)
    future_x = list(range(n, n + days_ahead))
    future_y = [m * x + b for x in future_x]

    # Create future date labels
    import datetime
    last_date = datetime.datetime.strptime(dates[-1], "%Y-%m-%d")
    future_dates = [
        (last_date + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d")
        for i in range(days_ahead)
    ]

    # Plot actual values
    plt.plot(dates, values, marker='o', linestyle='-', color='green', label="Actual Trend")

    # Plot forecast
    plt.plot(future_dates, future_y, marker='o', linestyle='--', color='red', label="Forecast")

    plt.title(f"Inventory Value Forecast ({days_ahead} Days Ahead)")
    plt.xlabel("Date")
    plt.ylabel("Total Inventory Value ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def chart_forecast_with_confidence(days_ahead=7, confidence=1.96):
    data = get_trend_data()
    if not data:
        print("No trend data available.")
        return

    dates = [row[0] for row in data]
    values = [row[1] for row in data]

    m, b = linear_regression_forecast(values)
    if m is None:
        print("Not enough data for forecasting.")
        return

    # Calculate variance
    variance = regression_variance(values, m, b)
    if variance is None:
        print("Not enough data for confidence intervals.")
        return

    n = len(values)
    future_x = list(range(n, n + days_ahead))
    future_y = [m * x + b for x in future_x]

    # Confidence interval width
    import math
    ci_width = confidence * math.sqrt(variance)

    upper = [y + ci_width for y in future_y]
    lower = [y - ci_width for y in future_y]

    # Create future dates
    import datetime
    last_date = datetime.datetime.strptime(dates[-1], "%Y-%m-%d")
    future_dates = [
        (last_date + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d")
        for i in range(days_ahead)
    ]

    # Plot actual trend
    plt.plot(dates, values, marker='o', linestyle='-', color='green', label="Actual Trend")

    # Plot forecast
    plt.plot(future_dates, future_y, marker='o', linestyle='--', color='red', label="Forecast")

    # Plot confidence intervals
    plt.fill_between(future_dates, lower, upper, color='orange', alpha=0.3, label="Confidence Interval")

    plt.title(f"Forecast with Confidence Interval ({days_ahead} Days Ahead)")
    plt.xlabel("Date")
    plt.ylabel("Total Inventory Value ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def chart_combined_forecast(window=3, days_ahead=7, confidence=1.96):
    data = get_trend_data()
    if not data:
        print("No trend data available.")
        return

    # Extract dates and values
    dates = [row[0] for row in data]
    values = [row[1] for row in data]

    # --- Moving Average ---
    ma_values = moving_average(values, window)
    ma_dates = dates[window - 1:] if ma_values else []

    # --- Linear Regression Forecast ---
    m, b = linear_regression_forecast(values)
    if m is None:
        print("Not enough data for forecasting.")
        return

    n = len(values)
    future_x = list(range(n, n + days_ahead))
    future_y = [m * x + b for x in future_x]

    # --- Confidence Interval ---
    variance = regression_variance(values, m, b)
    if variance is None:
        print("Not enough data for confidence intervals.")
        return

    import math
    ci_width = confidence * math.sqrt(variance)
    upper = [y + ci_width for y in future_y]
    lower = [y - ci_width for y in future_y]

    # --- Future Dates ---
    import datetime
    last_date = datetime.datetime.strptime(dates[-1], "%Y-%m-%d")
    future_dates = [
        (last_date + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d")
        for i in range(days_ahead)
    ]

    # --- Plotting ---
    plt.figure(figsize=(10, 6))

    # Actual trend
    plt.plot(dates, values, marker='o', linestyle='-', color='green', label="Actual Trend")

    # Moving average
    if ma_values:
        plt.plot(ma_dates, ma_values, marker='o', linestyle='-', color='blue', label=f"{window}-Day Moving Average")

    # Forecast line
    plt.plot(future_dates, future_y, marker='o', linestyle='--', color='red', label="Forecast")

    # Confidence interval shading
    plt.fill_between(future_dates, lower, upper, color='orange', alpha=0.3, label="Confidence Interval")

    plt.title("Combined Forecast Chart")
    plt.xlabel("Date")
    plt.ylabel("Total Inventory Value ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def export_combined_data_to_excel(window=3, days_ahead=7, confidence=1.96, filename="combined_forecast.xlsx"):
    data = get_trend_data()
    if not data:
        print("No trend data available.")
        return

    dates = [row[0] for row in data]
    values = [row[1] for row in data]

    # Moving average
    ma_values = moving_average(values, window)
    ma_dates = dates[window - 1:] if ma_values else []

    # Forecast
    m, b = linear_regression_forecast(values)
    if m is None:
        print("Not enough data for forecasting.")
        return

    n = len(values)
    future_x = list(range(n, n + days_ahead))
    future_y = [m * x + b for x in future_x]

    # Confidence interval
    variance = regression_variance(values, m, b)
    if variance is None:
        print("Not enough data for confidence intervals.")
        return

    import math
    ci_width = confidence * math.sqrt(variance)
    upper = [y + ci_width for y in future_y]
    lower = [y - ci_width for y in future_y]

    # Future dates
    import datetime
    last_date = datetime.datetime.strptime(dates[-1], "%Y-%m-%d")
    future_dates = [
        (last_date + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d")
        for i in range(days_ahead)
    ]

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Forecast Data"

    # Headers
    ws.append([
        "Date",
        "Actual Value",
        f"{window}-Day Moving Avg",
        "Forecast Date",
        "Forecast Value",
        "Upper Confidence",
        "Lower Confidence"
    ])

    # Actual + MA rows
    for i in range(len(dates)):
        ma_val = ma_values[i - (window - 1)] if i >= window - 1 else None
        ws.append([dates[i], values[i], ma_val, None, None, None, None])

    # Forecast rows
    for i in range(days_ahead):
        ws.append([
            None,
            None,
            None,
            future_dates[i],
            future_y[i],
            upper[i],
            lower[i]
        ])

    wb.save(filename)
    print(f"Combined forecast data exported to {filename}")

def chart_abc_analysis():
    data = abc_analysis()
    if not data:
        print("No product data available.")
        return

    names = [row[0] for row in data]
    values = [row[1] for row in data]
    categories = [row[3] for row in data]

    colors = []
    for c in categories:
        if c == "A":
            colors.append("red")
        elif c == "B":
            colors.append("orange")
        else:
            colors.append("green")

    plt.bar(names, values, color=colors)
    plt.title("ABC Analysis (Inventory Value by Product)")
    plt.xlabel("Product")
    plt.ylabel("Value ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def chart_pareto_analysis():
    data = pareto_analysis()
    if not data:
        print("No product data available.")
        return

    names = [row[0] for row in data]
    values = [row[1] for row in data]
    cumulative = [row[2] for row in data]

    fig, ax1 = plt.subplots()

    # Bar chart for product values
    ax1.bar(names, values, color='skyblue')
    ax1.set_xlabel("Products")
    ax1.set_ylabel("Value ($)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(rotation=45)

    # Line chart for cumulative percentage
    ax2 = ax1.twinx()
    ax2.plot(names, cumulative, color='red', marker='o')
    ax2.set_ylabel("Cumulative %", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.axhline(80, color='green', linestyle='--', label="80% Threshold")

    plt.title("Pareto Analysis (80/20 Rule)")
    fig.tight_layout()
    plt.show()

def chart_stockout_risk(daily_usage=1):
    data = stockout_risk(daily_usage)
    if not data:
        print("No product data available.")
        return

    names = [row[0] for row in data]
    days_left = [row[3] if row[3] is not None else 0 for row in data]
    risks = [row[4] for row in data]

    colors = []
    for r in risks:
        if r == "HIGH":
            colors.append("red")
        elif r == "MEDIUM":
            colors.append("orange")
        else:
            colors.append("green")

    plt.bar(names, days_left, color=colors)
    plt.title("Stockout Risk Prediction")
    plt.xlabel("Product")
    plt.ylabel("Days Until Stockout")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()





# -----------------------------
#   DASHBOARD VIEW
# -----------------------------

def view_dashboard():
    print("\n========== INVENTORY DASHBOARD ==========\n")

    print(f"Total Inventory Value: ${total_inventory_value():,.2f}")
    print(f"Total Products: {total_products()}")
    print(f"Low-Stock Items (<5): {low_stock_count()}")

    print("\n--- Inventory Value by Category ---")
    for name, value in inventory_value_by_category():
        print(f"{name}: ${value:,.2f}")

    print("\n--- Inventory Value by Supplier ---")
    for name, value in inventory_value_by_supplier():
        print(f"{name}: ${value:,.2f}")

    print("\n--- Top 5 Most Valuable Products ---")
    for name, value in top_5_products():
        print(f"{name}: ${value:,.2f}")

    print("\n=========================================\n")

    print("Charts Available:")
    print("1. Category Value Chart")
    print("2. Supplier Value Chart")
    print("3. Return to Dashboard Menu")

    choice = input("Choose an option: ")

    if choice == "1":
        chart_category_value()
    elif choice == "2":
        chart_supplier_value()
    else:
        return

def dashboard_menu():
    while True:
        print("\n========== DASHBOARD MENU ==========")
        print("1. View Dashboard Summary")
        print("2. Category Value Chart")
        print("3. Supplier Value Chart")
        print("4. Top 5 Products Chart")
        print("5. Save Daily Snapshot")
        print("6. Inventory Trend Chart")
        print("7. Moving Average Trend Chart")
        print("8. Forecast Line (Next 7 Days)")
        print("9. Forecast with Confidence Interval")
        print("10. Combined Forecast Chart")
        print("11. Export Combined Forecast Data to Excel")
        print("12. View ABC Analysis")
        print("13. ABC Analysis Chart")
        print("14. View Pareto Analysis")
        print("15. Pareto Chart (80/20)")
        print("16. View Stockout Risk")
        print("17. Stockout Risk Chart")
        print("18. Return to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            view_dashboard()
        elif choice == "2":
            chart_category_value()
        elif choice == "3":
            chart_supplier_value()
        elif choice == "4":
            chart_top_5_products()
        elif choice == "5":
            save_daily_snapshot()
        elif choice == "6":
            chart_inventory_trend()
        elif choice == "7":
            window = int(input("Enter moving average window (e.g., 3, 5, 7): "))
            chart_moving_average_trend(window)
        elif choice == "8":
            days = int(input("Forecast how many days ahead? "))
            chart_forecast_line(days)
        elif choice == "9":
            days = int(input("Forecast how many days ahead? "))
            chart_forecast_with_confidence(days)
        elif choice == "10":
            window = int(input("Moving average window (e.g., 3, 5, 7): "))
            days = int(input("Forecast days ahead: "))
            chart_combined_forecast(window, days)
        elif choice == "11":
            name = input("Enter Excel filename (default combined_forecast.xlsx): ")
            export_combined_data_to_excel(filename=name or "combined_forecast.xlsx")
        elif choice == "12":
            view_abc_analysis()
        elif choice == "13":
            chart_abc_analysis()
        elif choice == "14":
            view_pareto_analysis()
        elif choice == "15":
            chart_pareto_analysis()
        elif choice == "16":
            usage = int(input("Enter daily usage rate (default 1): ") or 1)
            view_stockout_risk(usage)
        elif choice == "17":
            usage = int(input("Enter daily usage rate (default 1): ") or 1)
            chart_stockout_risk(usage)
        elif choice == "18":
            break
        else:
            print("Invalid choice. Try again.")

