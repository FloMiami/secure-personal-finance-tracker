import sqlite3
import os
import pandas as pd
from pathlib import Path

class DBManager:
    def __init__(self, db_path="data/finance.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self._initialize_database()

    def _ensure_db_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def _initialize_database(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users (username)
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

    def get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def close_connection(self, conn):
        try:
            if conn:
                conn.close()
        except sqlite3.Error as e:
            print(f"Error closing the connection: {e}")

    def get_transactions(self, username):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, type, category, amount, description, date 
                FROM transactions WHERE username = ? ORDER BY date DESC
            """, (username,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching transactions: {e}")
            return []
        finally:
            conn.close()

    def export_to_excel(self, username):
        transactions = self.get_transactions(username)
        if not transactions:
            print("No transactions available for export.")
            return
        
        df = pd.DataFrame(transactions, columns=["ID", "Type", "Category", "Amount", "Description", "Date"])
        downloads_path = str(Path.home() / "Downloads")
        file_path = os.path.join(downloads_path, f"{username}_transactions.xlsx")
        
        df.to_excel(file_path, index=False)
        print(f"Transactions exported to Excel at {file_path}")

    def export_to_pdf(self, username):
        try:
            from fpdf import FPDF

            transactions = self.get_transactions(username)
            if not transactions:
                print("No transactions available for export.")
                return
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Financial Transactions Report", ln=True, align='C')
            
            for trans in transactions:
                pdf.cell(0, 10, txt=f"{trans}", ln=True)
            
            downloads_path = str(Path.home() / "Downloads")
            file_path = os.path.join(downloads_path, f"{username}_transactions.pdf")
            pdf.output(file_path)
            print(f"Transactions exported to PDF at {file_path}")
        except ImportError:
            print("fpdf module not installed. Install it using 'pip install fpdf'.")

    def generate_visual_insights(self, username):
        transactions = self.get_transactions(username)
        if not transactions:
            print("No transactions available for visual insights.")
            return

        df = pd.DataFrame(transactions, columns=["ID", "Type", "Category", "Amount", "Description", "Date"])
        summary = df.groupby("Type")["Amount"].sum()
        print("Visual insights:")
        print(summary)
