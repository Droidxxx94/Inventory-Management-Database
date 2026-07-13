
import pg8000

def get_connection():
    return pg8000.connect(
        database="inventory_db",
        user="u0_a829",
        password="your_password",
        host="localhost",
        port=5432
    )

