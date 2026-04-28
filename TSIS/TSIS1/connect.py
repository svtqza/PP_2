import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cur = conn.cursor()
    
    # 🔥 VERY IMPORTANT FIX
    cur.execute("SET search_path TO public;")

    # Optional debug (you can remove later)
    cur.execute("SELECT current_database(), current_schema();")
    print("CONNECTED TO:", cur.fetchone())

    cur.close()
    
    return conn