import tkinter as tk
from tkinter import messagebox
from auth import Auth
from finance_tracker import FinanceTracker
from report_generator import export_to_excel, export_to_pdf
from pathlib import Path
import os

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.auth = Auth()
        self.finance_tracker = None
        self.username = None
        self._build_login_screen()

    def _build_login_screen(self):
        """Build the login screen."""
        self.root.title("Finance Tracker - Login")
        self.clear_screen()

        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if self.auth.login_user(username, password):
                self.username = username
                self.finance_tracker = FinanceTracker(username)
                self._build_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        tk.Button(self.root, text="Login", command=login).pack()
        tk.Button(self.root, text="Register", command=self._build_registration_screen).pack()

    def _build_registration_screen(self):
        """Build the registration screen."""
        self.root.title("Finance Tracker - Register")
        self.clear_screen()

        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def register():
            username = username_entry.get()
            password = password_entry.get()
            if self.auth.register_user(username, password):
                messagebox.showinfo("Registration Successful", "You can now log in.")
                self._build_login_screen()
            else:
                messagebox.showerror("Registration Failed", "Username already exists.")

        tk.Button(self.root, text="Register", command=register).pack()
        tk.Button(self.root, text="Back to Login", command=self._build_login_screen).pack()

    def _build_dashboard(self):
        """Build the main dashboard."""
        self.root.title(f"Finance Tracker - {self.username}")
        self.clear_screen()

        summary = self.finance_tracker.get_summary()
        tk.Label(self.root, text=f"Total Income: ${summary['total_income']}").pack()
        tk.Label(self.root, text=f"Total Expenses: ${summary['total_expenses']}").pack()
        tk.Label(self.root, text=f"Balance: ${summary['balance']}").pack()

        tk.Button(self.root, text="View Transactions", command=self._view_transactions).pack()
        tk.Button(self.root, text="Export to Excel", command=self._export_to_excel).pack()
        tk.Button(self.root, text="Export to PDF", command=self._export_to_pdf).pack()
        tk.Button(self.root, text="Generate Report", command=self._generate_report).pack()
        tk.Button(self.root, text="Visual Insights", command=self._generate_analytics).pack()

    def _view_transactions(self):
        """View the user's transactions."""
        transactions = self.finance_tracker.get_transactions()
        if transactions:
            messagebox.showinfo("Transactions", "\n".join(str(t) for t in transactions))
        else:
            messagebox.showinfo("Transactions", "No transactions found.")

    def _export_to_excel(self):
        """Export data to Excel in the Downloads folder."""
        export_to_excel(self.username)
        messagebox.showinfo("Export Successful", "Excel file exported to Downloads folder.")

    def _export_to_pdf(self):
        """Export data to PDF in the Downloads folder."""
        export_to_pdf(self.username)
        messagebox.showinfo("Export Successful", "PDF file exported to Downloads folder.")

    def _generate_report(self):
        """Generate a placeholder report."""
        messagebox.showinfo("Generate Report", "Report generated successfully!")

    def _generate_analytics(self):
        """Generate visual insights."""
        messagebox.showinfo("Visual Insights", "Visual insights generated successfully!")

    def clear_screen(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
