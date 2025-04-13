import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox, 
    QTableWidget, QTableWidgetItem, QDialog, QStackedWidget
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

# Import your existing modules
from auth import Auth
from finance_tracker import FinanceTracker
from report_generator import export_to_excel, export_to_pdf
from db_manager import DBManager

class LoginWindow(QDialog):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth
        self.setWindowTitle("Finance Tracker - Login")
        self.setGeometry(300, 300, 400, 250)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Username Section
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password Section
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Button Layout
        button_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")
        
        login_btn.clicked.connect(self.login)
        register_btn.clicked.connect(self.register)
        
        button_layout.addWidget(login_btn)
        button_layout.addWidget(register_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #2C3E50;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #34495E;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if self.auth.login_user(username, password):
            self.finance_tracker = FinanceTracker(username)
            self.main_window = FinanceTrackerApp(self.finance_tracker, username)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if self.auth.register_user(username, password):
            QMessageBox.information(self, "Registration", "Account created successfully!")
        else:
            QMessageBox.warning(self, "Registration Failed", "Username already exists")

class FinanceTrackerApp(QMainWindow):
    def __init__(self, finance_tracker, username):
        super().__init__()
        self.finance_tracker = finance_tracker
        self.username = username
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Finance Tracker - {self.username}")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget and Main Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Retro Game Style Title
        title_label = QLabel("FINANCE TRACKER")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Press Start 2P', cursive;
                font-size: 36px;
                text-align: center;
                animation: rgb-strobe 1s linear infinite;
                text-shadow: 3px 3px 0px rgba(0,0,0,0.2);
            }
            @keyframes rgb-strobe {
                0% { color: red; text-shadow: 2px 2px 0 blue, -2px -2px 0 green; }
                33% { color: green; text-shadow: 2px 2px 0 red, -2px -2px 0 blue; }
                66% { color: blue; text-shadow: 2px 2px 0 green, -2px -2px 0 red; }
                100% { color: red; text-shadow: 2px 2px 0 blue, -2px -2px 0 green; }
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Welcome Label
        welcome_label = QLabel(f"Welcome, {self.username}")
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

        # Navigation Buttons
        nav_layout = QHBoxLayout()
        buttons_info = [
            ("Add Transaction", self.show_add_transaction),
            ("View Transactions", self.view_transactions),
            ("Visual Insights", self.visual_insights),
            ("Generate Report", self.generate_report),
            ("Export Excel", self.export_excel),
            ("Export PDF", self.export_pdf),
            ("Logout", self.logout)
        ]

        for label, method in buttons_info:
            btn = QPushButton(label)
            btn.clicked.connect(method)
            nav_layout.addWidget(btn)

        main_layout.addLayout(nav_layout)

        # Apply Professional Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
                color: white;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

    def show_add_transaction(self):
        # Implementation of add transaction dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Transaction")
        layout = QVBoxLayout()

        # Amount Input
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Amount:")
        amount_input = QLineEdit()
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(amount_input)
        layout.addLayout(amount_layout)

        # Category Input
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        category_input = QLineEdit()
        category_layout.addWidget(category_label)
        category_layout.addWidget(category_input)
        layout.addLayout(category_layout)

        # Type Selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        type_combo = QComboBox()
        type_combo.addItems(["income", "expense"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(type_combo)
        layout.addLayout(type_layout)

        # Save Button
        save_btn = QPushButton("Save Transaction")
        save_btn.clicked.connect(lambda: self.save_transaction(
            amount_input.text(), 
            category_input.text(), 
            type_combo.currentText(),
            dialog
        ))
        layout.addWidget(save_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_transaction(self, amount, category, type_, dialog):
        try:
            amount = float(amount)
            if not category:
                raise ValueError("Category cannot be empty")
            
            self.finance_tracker.add_transaction(type_, category, amount)
            QMessageBox.information(self, "Success", "Transaction added successfully!")
            dialog.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def view_transactions(self):
        transactions = self.finance_tracker.get_transactions()
        dialog = QDialog(self)
        dialog.setWindowTitle("Transactions")
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Type", "Category", "Amount", "Description", "Date"])
        table.setRowCount(len(transactions))

        for row, transaction in enumerate(transactions):
            for col, value in enumerate(transaction):
                table.setItem(row, col, QTableWidgetItem(str(value)))

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()

    def visual_insights(self):
        data = self.finance_tracker.get_transactions()
        df = pd.DataFrame(data, columns=['ID', 'Type', 'Category', 'Amount', 'Description', 'Date'])
        
        category_summary = df.groupby(['Type', 'Category'])['Amount'].sum().unstack(fill_value=0)
        
        income_categories = category_summary.loc['income'] if 'income' in category_summary.index else pd.Series()
        expense_categories = category_summary.loc['expense'] if 'expense' in category_summary.index else pd.Series()

        plt.figure(figsize=(12, 6))
        bar_width = 0.35
        index = range(len(set(income_categories.index) | set(expense_categories.index)))
        
        plt.bar(index, income_categories, bar_width, label='Income', color='green', alpha=0.7)
        plt.bar([i + bar_width for i in index], expense_categories, bar_width, label='Expenses', color='red', alpha=0.7)
        
        plt.xlabel('Categories', fontsize=10)
        plt.ylabel('Amount ($)', fontsize=10)
        plt.title('Financial Insights: Income vs Expenses by Category', fontsize=12)
        plt.xticks([i + bar_width/2 for i in index], 
                   list(set(income_categories.index) | set(expense_categories.index)), 
                   rotation=45, 
                   ha='right')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def generate_report(self):
        summary = self.finance_tracker.get_summary()
        report = (f"Total Income: ${summary['total_income']}\n"
                  f"Total Expenses: ${summary['total_expenses']}\n"
                  f"Balance: ${summary['balance']}")
        QMessageBox.information(self, "Financial Report", report)

    def export_excel(self):
        export_to_excel(self.username)
        QMessageBox.information(self, "Export", "Excel report exported successfully!")

    def export_pdf(self):
        export_to_pdf(self.username)
        QMessageBox.information(self, "Export", "PDF report exported successfully!")

    def logout(self):
        self.close()
        login_window = LoginWindow(Auth())
        login_window.show()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow(Auth())
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()