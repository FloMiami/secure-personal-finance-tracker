import hashlib
import sqlite3
from db_manager import DBManager
from tkinter import messagebox  # To provide GUI feedback on actions

class Auth:
    def __init__(self):
        self.db_manager = DBManager()

    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """
        Register a new user with a hashed password.
        :param username: The desired username
        :param password: The password to be hashed and stored
        :return: True if registration is successful, False if username exists
        """
        hashed_password = self.hash_password(password)
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()

        try:
            # Check if username already exists
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Registration Failed", "Username already exists.")
                return False

            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return False
        finally:
            conn.close()

    def login_user(self, username, password):
        """
        Log in a user by checking the hashed password.
        :param username: The username
        :param password: The plaintext password to verify
        :return: True if login is successful, False otherwise
        """
        hashed_password = self.hash_password(password)
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

            if row and row[0] == hashed_password:
                messagebox.showinfo("Login Success", f"Welcome back, {username}!")
                return True
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
                return False
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return False
        finally:
            conn.close()


