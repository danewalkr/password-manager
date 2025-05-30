# Password Manager App

A simple, beginner-friendly password manager application built with Python. Features a modern GUI using `ttkbootstrap`, local encrypted storage using SQLite, and password generation.

## Features

- Modern GUI with `ttkbootstrap` themes
- Add and encrypt website credentials (service, username, password)
- AES-based encryption with `cryptography.Fernet`
- Random password generator with symbols, digits, and letters
- View saved passwords securely in a separate window
- Local storage using SQLite database

## How to Use

1. **Clone the repository**  
   ```bash
   git clone https://github.com/danewalkre/password-manager-app.git
   cd password-manager-app
   ```

2. **Install dependencies**  
   Use the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**  
   ```bash
   python app.py
   ```

## Dependencies

- `tkinter` (included with most Python 3 installations)
- [`ttkbootstrap`](https://ttkbootstrap.readthedocs.io/en/latest/)
- [`cryptography`](https://pypi.org/project/cryptography/)
