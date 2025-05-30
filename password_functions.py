import ttkbootstrap as tb
import tkinter as tk
import sqlite3
import random, string
from cryptography.fernet import Fernet
import os

class PasswordManagement:
    def __init__(self, app):
            self.app = app
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(BASE_DIR, "password_manager.db")
            self.key_path = os.path.join(BASE_DIR, "key.key")

            
            # Load or generate key
            if os.path.exists(self.key_path):
                with open(self.key_path, 'rb') as f:
                    self.key = f.read()
            else:
                self.key = Fernet.generate_key()
                os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
                with open(self.key_path, 'wb') as f:
                    f.write(self.key)

            self.fernet = Fernet(self.key)
                
    def setup_database(self):
            """Ensures database file exists"""
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS passwords (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            service TEXT NOT NULL,
                            username TEXT NOT NULL,
                            password BLOB NOT NULL
                        )
                    ''')
                    conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred while setting up the database: {e}")
                return e

    def encrypt_passwords(self, plain_password):
            try:
                if isinstance(plain_password, str):
                    plain_password = plain_password.encode()
                encrypted_password = self.fernet.encrypt(plain_password)
                return encrypted_password
            except ValueError as e:
                print(f"Error encrypting password: {e}")
                raise
    
    def decrypt_passwords(self, encrypted_password):
            try:
                decrypted = self.fernet.decrypt(encrypted_password)
                return decrypted.decode()
            except Exception as e:
                print(f"Error decrypting password: {e}")
                raise

    def save_data(self, entries):
            """Saves a list of password entries to the database after encryption."""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for entry in entries:
                    service = entry['service']
                    username = entry['username']
                    password = entry['password']
                    encrypted_password = self.encrypt_passwords(password)

                    cursor.execute('''
                        INSERT INTO passwords (service, username, password)
                        VALUES (?, ?, ?)
                    ''', (service, username, encrypted_password))
                conn.commit()

    def load_data(self):
            """Decrypts a list of password entries from the database and loads them."""
            decrypted_entries = []
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT service, username, password FROM passwords")
                rows = cursor.fetchall()

                for service, username, encrypted_password in rows:
                    decrypted_password = self.decrypt_passwords(encrypted_password)
                    decrypted_entries.append({
                        'service': service,
                        'username': username,
                        'password': decrypted_password
                    })

            return decrypted_entries

    def current_status(self, status):
            """Displays and updates the status label"""
            if status == 'Idle...':
                self.app.status_label.config(text=f"Status: {status}", bootstyle="secondary") 
            elif status == 'Generating...':
                self.app.status_label.config(text=f"Status: {status}", bootstyle="info")  
            elif status == "Submitted...":
                self.app.status_label.config(text=f"Status: {status}", bootstyle="success") 
            elif status == "Viewing...":
                self.app.status_label.config(text=f"Status: {status}", bootstyle="primary")
            elif status == "All fields must be filled...":
                self.app.status_label.config(text=f"Status: {status}", bootstyle="danger")
       
    def generate_function(self, length=12):
            """Generates a random 12 letter password"""
            characters = string.ascii_letters + string.digits + '!$?'
            self.current_status("Generating...")
            password = ''.join(random.choice(characters) for _ in range(length))
            self.app.password_entry.delete(0, 'end')
            self.app.password_entry.insert(0, password)
            return password
    
    def submit_function(self):
            """Handles data entry"""
            service = self.app.website_entry.get().strip()
            username = self.app.user_entry.get().strip()
            password = self.app.password_entry.get().strip()

            
            if not service or not username or not password:
                self.current_status("All fields must be filled...")
                return
            else:
                self.current_status("Submitted...")

            new_entry = {
                'service': service,
                'username': username,
                'password': password
            }

            # Save new entry
            self.save_data([new_entry])

            # Loads and print updated data
            all_entries = self.load_data()
            print("Current entries:")
            for entry in all_entries:
                print(entry)
            
            self.app.website_entry.delete(0, 'end')
            self.app.user_entry.delete(0, 'end')
            self.app.password_entry.delete(0, 'end')
            
    def view_passwords(self):
            """View user data"""
            self.current_status("Viewing...")
            
            # Create the root window
            self.root = tb.Window(themename="cosmo")
            self.root.title("View Saved Passwords")
            self.root.geometry("600x450")
            self.root.resizable(False, False)

            # Creates the main frame
            self.main_frame = tb.Frame(self.root, padding=20)
            self.main_frame.pack(expand=True, fill="both", side="top")

            #  Create widgets displaying data
            self.create_widgets()

            # Tkinter event loop
            self.root.mainloop()

    def create_widgets(self):
            """View frame widgets"""
            data = self.load_data()
            
            heading = tb.Label(
                self.main_frame, 
                text="Saved Passwords!", 
                font=("Segoe UI", 26, "bold"), 
                foreground="#007bff" 
            )
            heading.pack(pady=(0, 5))

            subtitle = tb.Label(
                self.main_frame,
                text="Select a service to view credentials",
                font=("Segoe UI", 11, "italic"),
                foreground="gray"
            )
            subtitle.pack(pady=(0, 20))

            # Paned window for layout
            paned_window = tk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
            paned_window.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

            # Frame for the listbox
            list_frame = tb.Frame(paned_window, padding=10)
            paned_window.add(list_frame, width=200)

            listbox_label = tb.Label(list_frame, text="Websites", font=("Segoe UI", 12, "bold"))
            listbox_label.pack(anchor='w', padx=(5, 0))

            listbox = tk.Listbox(list_frame, width=25, height=15, font=("Segoe UI", 11))
            listbox.pack(side=tk.LEFT, fill=tk.Y, pady=5)

            scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
            scrollbar.config(command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)

            for entry in data:
                listbox.insert(tk.END, entry['service'])

            # Detail frame
            detail_frame = tb.Frame(paned_window, padding=20)
            paned_window.add(detail_frame, width=360)

            # Labels
            username_title = tb.Label(detail_frame, text="Email/Username", font=("Segoe UI", 10, "bold"))
            username_title.pack(anchor='w')
            username_display = tb.Entry(detail_frame, font=("Segoe UI", 11), state='readonly', width=35)
            username_display.pack(anchor='w', pady=(0, 10))

            password_title = tb.Label(detail_frame, text="Password", font=("Segoe UI", 10, "bold"))
            password_title.pack(anchor='w')
            password_display = tb.Entry(detail_frame, font=("Segoe UI", 11), state='readonly', width=35)
            password_display.pack(anchor='w')

            def show_details(event):
                selected_index = listbox.curselection()
                if selected_index:
                    selected_site = data[selected_index[0]]
                    username_display.config(state='normal')
                    password_display.config(state='normal')
                    username_display.delete(0, tk.END)
                    password_display.delete(0, tk.END)
                    username_display.insert(0, selected_site['username'])
                    password_display.insert(0, selected_site['password'])
                    username_display.config(state='readonly')
                    password_display.config(state='readonly')

            listbox.bind("<<ListboxSelect>>", show_details)