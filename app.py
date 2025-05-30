import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from password_functions import PasswordManagement

class PasswordApp():
    def __init__(self):
        self.root = tb.Window(themename="cosmo")
        self.root.title("Password Manager App V.1")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.main_frame = tb.Frame(self.root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.create_widgets()
        self.manager = PasswordManagement(self)
        self.manager.setup_database()

        self.root.mainloop()

    def create_widgets(self):
        # Fonts
        title_font = ("Segoe UI", 28, "bold")
        subtext_font = ("Segoe UI", 14, "italic")
        entry_font = ("Segoe UI", 12)
        
        # Title
        title_label = tb.Label(self.main_frame, text="Password Manager!", font=title_font, bootstyle="primary")
        title_label.pack(pady=(10, 5))

        # Sub-text
        sub_text_label = tb.Label(self.main_frame, text="Simple encryption app to store passwords safely", font=subtext_font, bootstyle="secondary")
        sub_text_label.pack(pady=(0, 25))

        # Entry frame
        entry_frame = tb.Frame(self.main_frame)
        entry_frame.pack(pady=5, fill=X)

        # Website Entry
        website_label = tb.Label(entry_frame, text="Website :", font=entry_font)
        website_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.website_entry = tb.Entry(entry_frame, font=entry_font, width=30)
        self.website_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

        # Email/Username Entry
        user_label = tb.Label(entry_frame, text="Email/Username :", font=entry_font)
        user_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.user_entry = tb.Entry(entry_frame, font=entry_font, width=30)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

        # Frame that holds password entry and toggle button
        password_frame = tb.Frame(entry_frame)
        password_frame.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Password Entry and Generate Button
        self.password_visible = False
        password_label = tb.Label(entry_frame, text="Password :", font=entry_font)
        password_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tb.Entry(password_frame, font=entry_font, show="*", width=25)
        self.password_entry.pack(side="left", fill="x", expand=True)
        password_generate = tb.Button(entry_frame, text="Generate", bootstyle="danger", command=self.generate_wrapper)
        password_generate.grid(row=2, column=2, padx=5, pady=5)

        # Show/Hide toggle button
        def toggle_password():
            self.password_visible = not self.password_visible
            self.password_entry.config(show="" if self.password_visible else "*")
            toggle_btn.config(text="🙈" if self.password_visible else "👁")

        toggle_btn = tb.Button(password_frame, text="👁", width=3, command=toggle_password, bootstyle="secondary")
        toggle_btn.pack(side="left", padx=(5, 0))

        # Buttons Frame
        btn_frame = tb.Frame(self.main_frame)
        btn_frame.pack(pady=20)

        submit_btn = tb.Button(btn_frame, text="Submit", width=15, bootstyle="success", command=self.submit_wrapper)
        submit_btn.grid(row=0, column=0, padx=10)

        view_btn = tb.Button(btn_frame, text="View", width=15, bootstyle="info", command=self.view_wrapper)
        view_btn.grid(row=0, column=1, padx=10)
        
        # Status label at the bottom
        self.status_label = tb.Label(self.main_frame, text="Status: Idle...", bootstyle="warning")
        self.status_label.pack(pady=(10, 0))

    def generate_wrapper(self):
        self.manager.generate_function()

    def submit_wrapper(self):
        self.manager.submit_function()
        
    def view_wrapper(self):
        self.manager.view_passwords()

    def current_status(self, status):
        self.status_label.config(text=f"Status: {status}")

if __name__ == "__main__":
    app = PasswordApp()