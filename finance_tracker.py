import os
import sqlite3
from db_manager import DBManager
from datetime import datetime
import pandas as pd  # For exporting to Excel and PDF

class FinanceTracker:
    def __init__(self, username):
        self.username = username
        self.db_manager = DBManager()
        self.downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    def add_transaction(self, trans_type, category, amount, description="", date=None):
        if trans_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be either 'income' or 'expense'.")
        if amount < 0:
            raise ValueError("Transaction amount must be non-negative.")
        date = date or datetime.now().strftime('%Y-%m-%d')
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (username, type, category, amount, description, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.username, trans_type, category, amount, description, date))
            conn.commit()
            print("Transaction added successfully.")
        except Exception as e:
            print(f"Error adding transaction: {e}")
        finally:
            conn.close()

    def get_transactions(self, limit=None):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            query = """
                SELECT id, type, category, amount, description, date
                FROM transactions
                WHERE username = ?
                ORDER BY date DESC
            """
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query, (self.username,))
            transactions = cursor.fetchall()
            print("Transactions retrieved successfully.")
            return transactions
        except Exception as e:
            print(f"Error retrieving transactions: {e}")
            return []
        finally:
            conn.close()

    def generate_summary(self):
        summary = self.get_summary()
        print(f"Total Income: {summary['total_income']}")
        print(f"Total Expenses: {summary['total_expenses']}")
        print(f"Balance: {summary['balance']}")
        print("Report generated successfully.")

    def export_to_excel(self):
        transactions = self.get_transactions()
        df = pd.DataFrame(transactions, columns=['ID', 'Type', 'Category', 'Amount', 'Description', 'Date'])
        filepath = os.path.join(self.downloads_folder, f"{self.username}_transactions.xlsx")
        df.to_excel(filepath, index=False)
        print(f"Transactions exported to Excel: {filepath}")

    def export_to_pdf(self):
        transactions = self.get_transactions()
        df = pd.DataFrame(transactions, columns=['ID', 'Type', 'Category', 'Amount', 'Description', 'Date'])
        filepath = os.path.join(self.downloads_folder, f"{self.username}_transactions.pdf")
        df.to_html("temp.html")  # Save as HTML first
        os.system(f"wkhtmltopdf temp.html {filepath}")  # Convert HTML to PDF using wkhtmltopdf
        os.remove("temp.html")  # Clean up temp file
        print(f"Transactions exported to PDF: {filepath}")

    def get_summary(self):
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(amount) FROM transactions
                WHERE username = ? AND type = 'income'
            """, (self.username,))
            total_income = cursor.fetchone()[0] or 0
            cursor.execute("""
                SELECT SUM(amount) FROM transactions
                WHERE username = ? AND type = 'expense'
            """, (self.username,))
            total_expenses = cursor.fetchone()[0] or 0
            return {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "balance": total_income - total_expenses
            }
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {"total_income": 0, "total_expenses": 0, "balance": 0}
        finally:
            conn.close()

    def get_data(self):
        """Retrieve data for visualization or analysis."""
        transactions = self.get_transactions()
        data = pd.DataFrame(transactions, columns=['ID', 'Type', 'Category', 'Amount', 'Description', 'Date'])
        print("Data retrieved successfully for visualization.")
        return data

    def view_transactions(self):
        transactions = self.get_transactions()
        for trans in transactions:
            print(f"ID: {trans[0]}, Type: {trans[1]}, Category: {trans[2]}, Amount: {trans[3]}, Date: {trans[5]}")
        print("Transactions displayed successfully.")
