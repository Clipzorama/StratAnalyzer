import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from loader import LoaderPage
from hashlib import pbkdf2_hmac
import os  # Module used
import sqlite3


class LoginApp:

    def __init__(self):

        self.login_win = tk.Tk()

        self.login_win.overrideredirect(1)

        # Dimensions of the window
        width_of_window = 427
        height_of_window = 250

        # Fixed screen dimensions
        screen_width = self.login_win.winfo_screenwidth()
        screen_height = self.login_win.winfo_screenheight()

        x_coordinate = (screen_width // 2) - (width_of_window // 2)
        y_coordinate = (screen_height // 2) - (height_of_window // 2)

        self.login_win.geometry(
            "%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.login_win.configure(bg='#040200')

        login_label = tk.Label(self.login_win, text="TA Login", font=(
            'Super Funtime', 30), fg="#f5f5dc", bg='#040200')
        username_label = tk.Label(self.login_win, text="Username:", font=(
            'Arial', 16), bg='#040200', fg='#f5f5dc')
        self.username_entry = tk.Entry(self.login_win, fg='#040200', show="*")
        password_label = tk.Label(self.login_win, text="Password:", font=(
            "Arial", 16), bg='#040200', fg='#f5f5dc')
        self.password_entry = tk.Entry(self.login_win, show="*", fg='#040200')
        auth_button = ctk.CTkButton(self.login_win, text="Login", font=("Arial", 16),
                                    bg_color='#040200', fg_color='#5d382f',
                                    hover_color='#422A25', command=self.login)

        login_label.place(x=155, y=25)
        username_label.place(x=67, y=95)
        self.username_entry.place(x=153, y=95)
        password_label.place(x=67, y=135)
        self.password_entry.place(x=153, y=135)
        auth_button.place(x=150, y=200)

    def login(self):

        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        # Retrieve the stored hashed password for the entered username
        stored_hashed_pwd = self.get_stored_hashed_password(entered_username)
        destroyu = "0"
        destroyp = "0"

        # If stored password is present in database with given username, and also verified password is true with the input and stored password
        if stored_hashed_pwd and self.verify_password(stored_hashed_pwd, entered_password):
            messagebox.showinfo(title="Login Success",
                                message="You successfully logged in!")
            self.loader_segue()

        elif self.username_entry.get() == destroyu and self.password_entry.get() == destroyp:
            self.login_win.destroy()
        else:
            print("Invalid Password")

    # Need a method that hashes passwords. This way, we can hash the password when we insert a new user.

    def hash_password(self, password):

        # Generates a string of random by
        salt = os.urandom(16)
        # Converts the password string in byte format
        # Goes through hash algorthm 100000 times
        hash = pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt, 100000)

        return salt + hash

    def insert_user(self, username, password):
        # Using the sqlite3 module to connect to the database
        conn = sqlite3.connect('password.db')
        cursor = conn.cursor()

        try:
            # Creating the table here. That displays the users username with hashed password. Will make it easier to access both propertoes
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                hashed_password TEXT 
            )
            ''')
            conn.commit()  # Adds execution the database

            # Checking if the user already exists. Parameter is in the format of a tuple
            # Checking if the username matches the one in the database
            cursor.execute(
                "SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():  # If the cursor fetches this data inside of the table
                print(f"Error: Username '{username}' already exists.")
            else:
                # User does not exist, proceed with inserting new user. Here we are hashing the password that is in the password parameter.
                # Hex format for readability in database. Convert back to byte when verifying password
                hashed_password = self.hash_password(password).hex()
                cursor.execute(
                    'INSERT INTO users (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
                conn.commit()  # Adds the new user inside of the database
                print(f"User '{username}' created successfully.")

        # Error takes care of database / connection issues.
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def verify_password(self, stored_password, provided_password):

        # Convert stored password from hex to bytes
        stored_password_bytes = bytes.fromhex(stored_password)

        # Salt for the stored password is recalled to compared with the provided password to see if both hash values are the same
        # Extracting the salt from stored so it isnt randomized everytime
        salt = stored_password_bytes[:16]

        # Extract stored hash (remaining bytes)
        stored_hash = stored_password_bytes[16:]

        # Iterates 100000 to slow down the key derivation process intentionally for more security.
        hshpwd = pbkdf2_hmac('sha256', bytes(
            provided_password, 'utf-8'), salt, 100000)

        return hshpwd == stored_hash  # Checks boolean to execute next condition

    def get_stored_hashed_password(self, username):
        try:
            conn = sqlite3.connect('password.db')
            cursor = conn.cursor()

            # Looking for the hashed password. Username as reference. Comma after since its in a tuple and the program knows that
            cursor.execute(
                "SELECT hashed_password FROM users WHERE username = ?", (username,))
            # Password in database turns into an object that we would then return once the username parameter is passed
            result = cursor.fetchone()

            conn.close()

            if result:
                # Return the stored hashed password as a hex string which would then be converted to byte format to compare
                return result[0]
            else:
                # Return None if the username is not found
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def delete_user(self, username):
        try:
            # Its always to connect and close the database everytime you have intentions of opening .
            conn = sqlite3.connect('password.db')
            cursor = conn.cursor()

            # Delete the user from the database
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            print(f"User '{username}' deleted successfully.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def new_win(self):
        from tsla import TSLACC
        file = 'Data/TSLA_5min.csv'
        app = TSLACC(file)
        self.loading.close()
        self.login_win.destroy()
        app.run()

    def loader_segue(self):
        self.loading = LoaderPage()
        # Here I can call the method from a new method in login
        self.loading.segue(self.new_win)

    def runner(self):
        self.login_win.mainloop()


app = LoginApp()
app.runner()
