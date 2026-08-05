def get_inventory_value(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(quantity * unit_price) AS total_value
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
    cur = conn.cursor()
    cur.execute("""
        SELECT suppliers.name, COUNT(*)
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        GROUP BY suppliers.name
    """)
    return cur.fetchall()


def get_category_summary(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT categories.name, COUNT(*) AS num_items
        FROM products
        LEFT JOIN categories ON products.category_id = categories.id
        GROUP BY categories.name;
    """)
    return cursor.fetchall()


def get_top_value_products(conn, limit=5):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, quantity, unit_price
        FROM products
        ORDER BY quantity * unit_price DESC
        LIMIT ?;
    """, (limit,))
    return cursor.fetchall()


