def get_inventory_value(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(quantity * price) AS total_value
        FROM products;
    """)
    return cursor.fetchone()[0]

def get_low_stock_items(conn, threshold=5):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, quantity
        FROM products
        WHERE quantity <= ?;
    """, (threshold,))
    return cursor.fetchall()

def get_supplier_counts(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT supplier, COUNT(*) AS product_count
        FROM products
        GROUP BY supplier;
    """)
    return cursor.fetchall()

def get_category_summary(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, COUNT(*) AS num_items
        FROM products
        GROUP BY category;
    """)
    return cursor.fetchall()

def get_top_value_products(conn, limit=5):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, quantity * price AS value
        FROM products
        ORDER BY value DESC
        LIMIT ?;
    """, (limit,))
    return cursor.fetchall()

