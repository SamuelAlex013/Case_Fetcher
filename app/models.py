import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'court_case.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT NOT NULL,
                case_number TEXT NOT NULL,
                filling_year INTEGER NOT NULL,
                time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_response TEXT)
    ''')
    conn.commit()
    conn.close()

def insert_query(case_type, case_number, filling_year, raw_response):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO queries (case_type, case_number, filling_year, raw_response)
    VALUES (?, ?, ?, ?)
    ''', (case_type, case_number, filling_year, raw_response))
    conn.commit()
    cur.execute('''
    SELECT * from queries
    ''')
    
    conn.commit()
    conn.close()