import pandas as pd
from fpdf import FPDF
from db_manager import DBManager
from pathlib import Path
import os

def export_to_excel(username):
    """
    Export transactions to an Excel file for the specified user.
    :param username: The username of the user
    """
    db_manager = DBManager()
    conn = db_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE username = ?", (username,))
    rows = cursor.fetchall()

    # Define column names for Excel
    columns = ["ID", "Username", "Type", "Category", "Amount", "Date", "Description"]

    if not rows:
        print(f"No transactions found for {username}.")
        return

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Save to Excel file in Downloads folder
    downloads_path = str(Path.home() / "Downloads")
    file_path = os.path.join(downloads_path, f"{username}_transactions.xlsx")
    df.to_excel(file_path, index=False)

    conn.close()
    print(f"Transactions successfully exported to Excel at {file_path}")

def export_to_pdf(username):
    """
    Export transactions to a PDF file for the specified user.
    :param username: The username of the user
    """
    db_manager = DBManager()
    conn = db_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT type, category, amount, date, description FROM transactions WHERE username = ?", (username,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"No transactions found for {username}.")
        return

    # Initialize PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt=f"{username}'s Transaction Report", ln=True, align='C')
    pdf.ln(10)

    # Add table headers
    pdf.set_font("Arial", size=12, style="B")
    headers = ["Type", "Category", "Amount", "Date", "Description"]
    column_widths = [40, 40, 30, 30, 50]
    for i, header in enumerate(headers):
        pdf.cell(column_widths[i], 10, header, border=1)
    pdf.ln()

    # Add table rows
    pdf.set_font("Arial", size=12)
    for row in rows:
        pdf.cell(40, 10, row[0], border=1)
        pdf.cell(40, 10, row[1], border=1)
        pdf.cell(30, 10, f"${row[2]:.2f}", border=1)
        pdf.cell(30, 10, row[3], border=1)
        pdf.cell(50, 10, row[4], border=1)
        pdf.ln()

    # Save to PDF file in Downloads folder
    downloads_path = str(Path.home() / "Downloads")
    file_path = os.path.join(downloads_path, f"{username}_transactions.pdf")
    pdf.output(file_path)

    print(f"Transactions successfully exported to PDF at {file_path}")

# Ensure these functions are properly accessible
__all__ = ["export_to_excel", "export_to_pdf"]

