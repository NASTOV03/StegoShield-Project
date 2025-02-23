import json
import os
import time
import datetime
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, ttk, StringVar, Text, Scrollbar, Canvas
from encryption import encrypt_message
from decryption import decrypt_message

# Load Credentials from External Configuration File
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"username": "admin", "password": "admin123"}
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(new_data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(new_data, file, indent=4)

config = load_config()

# File Selection
def select_file(entry_var):
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Supported Files", "*.png;*.jpg;*.mp3;*.wav;*.mp4;*.avi")])
    if file_path:
        entry_var.set(file_path)

# Encoding
def encode():
    start_time = time.time()
    file_path, message, key = entry_file_path.get(), entry_msg.get(), entry_key.get()

    # Logging before process starts
    log_activity("Encrypting a file............/-", "N/A", 0, "Starting encryption process")

    if not (file_path and message and key):
        return messagebox.showwarning("Error", "Please select a file, enter a message, and a key.")
    
    encrypted_msg = encrypt_message(message, key)
    with open(file_path, 'rb') as f:
        data = f.read() + b"--ENCRYPTED--" + encrypted_msg.encode()
    with open("encrypted_output" + os.path.splitext(file_path)[-1], 'wb') as f:
        f.write(data)

    time_taken = round(time.time() - start_time, 2)
    file_type= os.path.splitext(file_path)[-1]
    log_activity("Encrypted a file", file_type, time_taken, "File encryption completed.")

    messagebox.showinfo("Success", "File encrypted successfully!")
    entry_file_path.set("")
    entry_msg.set("")
    entry_key.set("")

# Decoding
def decode():
    start_time = time.time()
    file_path, key = entry_file_path_decrypt.get(), entry_key_decrypt.get()

    # Logging before process starts
    log_activity("Decrypting a file............/-", "N/A", 0, "Starting decryption process")

    
    if not (file_path and key):
        return messagebox.showwarning("Error", "Please select a file and enter the decryption key.")
    
    with open(file_path, 'rb') as f:
        extracted_msg = f.read().split(b"--ENCRYPTED--")[-1].decode(errors='ignore')
    decrypted_msg = decrypt_message(extracted_msg, key)

    time_taken = round(time.time() - start_time, 2)
    file_type= os.path.splitext(file_path)[-1]
    log_activity("Decrypted a file", file_type, time_taken, "File decryption completed.")

    messagebox.showinfo("Decryption Result", decrypted_msg)

    entry_file_path_decrypt.set("")
    entry_key_decrypt.set("")

# Authentication
def login():
    if username.get() == config["username"] and password.get() == config["password"]:
        login_window.destroy()  
        show_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

# Update Credentials in Config File
def update_credentials():
    global config
    new_username = new_username_var.get()
    new_password = new_password_var.get()

    if new_username:
        config["username"] = new_username
    if new_password:
        config["password"] = new_password

    save_config(config)
    current_username.set(config["username"])  # Update UI with new username
    messagebox.showinfo("Success", "Credentials updated successfully!")

# Show Main UI after login
def show_main_window():
    global root, log_display, entry_file_path, entry_msg, entry_key, entry_file_path_decrypt, entry_key_decrypt
    global new_username_var, new_password_var, current_username

    root = Tk()
    root.title("Steganography Encryption Tool")
    root.geometry("600x450")
    root.configure(bg="#2c3e50")

    # Adding Watermark Using Canvas
    canvas = Canvas(root, width=600, height=40, bg="#2c3e50", highlightthickness=0)
    canvas.pack(side="bottom", fill="x")
    canvas.create_text(300, 25, text="© 2025 Steganography Encryption Tool by Vivek Kumar Yadav", font=("Arial", 12, "italic"), fill="gray")
    
    notebook = ttk.Notebook(root)
    tab_encrypt = ttk.Frame(notebook)
    tab_decrypt = ttk.Frame(notebook)
    tab_logs = ttk.Frame(notebook)
    tab_settings = ttk.Frame(notebook)

    notebook.add(tab_encrypt, text="Encrypt")
    notebook.add(tab_decrypt, text="Decrypt")
    notebook.add(tab_logs, text="Logging & Reporting")
    notebook.add(tab_settings, text="Settings")

    entry_file_path, entry_msg, entry_key = StringVar(), StringVar(), StringVar()
    entry_file_path_decrypt, entry_key_decrypt = StringVar(), StringVar()

    # Encryption Tab
    Label(tab_encrypt, text="Select File:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
    Entry(tab_encrypt, textvariable=entry_file_path, width=50).pack()
    Button(tab_encrypt, text="Browse", font=("Arial", 12), command=lambda: select_file(entry_file_path)).pack(pady=(0,30))
    
    Label(tab_encrypt, text="Enter Message:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=(10,10))
    Entry(tab_encrypt, textvariable=entry_msg, width=50).pack(pady=(0,30))
    
    Label(tab_encrypt, text="Enter Key:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
    Entry(tab_encrypt, textvariable=entry_key, width=50, show="*").pack()
    Button(tab_encrypt, text="Encrypt", font=("Arial", 12), command=encode).pack(pady=10)

    # Decryption Tab
    Label(tab_decrypt, text="Select File:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
    Entry(tab_decrypt, textvariable=entry_file_path_decrypt, width=50).pack()
    Button(tab_decrypt, text="Browse", font=("Arial", 12), command=lambda: select_file(entry_file_path_decrypt)).pack(pady=(10,30))
    
    Label(tab_decrypt, text="Enter Key:",font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
    Entry(tab_decrypt, textvariable=entry_key_decrypt, width=50, show="*").pack()
    Button(tab_decrypt, text="Decrypt",font=("Arial", 12), command=decode).pack(pady=10)

    # Logging Tab with Text widget
    global log_text
    log_text = StringVar()
    Label(tab_logs, text="Activity Log", font=("Arial", 14), bg="#2c3e50", fg="white").pack(pady=5)

    # Create a Text widget with a Scrollbar
    log_display = Text(tab_logs, wrap="word", width=90, height=120, bg="#2c3e50", fg="white", font=("Arial", 10), padx=10, pady=10)
    log_display.pack(pady=10)

    # Adding a Scrollbar
    scrollbar = Scrollbar(tab_logs, command=log_display.yview)
    scrollbar.pack(side="right", fill="y")
    log_display.config(yscrollcommand=scrollbar.set)

    # Settings Tab
    current_username = StringVar(value=config["username"])
    new_username_var, new_password_var = StringVar(), StringVar()

    Label(tab_settings, text="Current Username:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
    Label(tab_settings, textvariable=current_username, fg="blue", font=("Arial", 12)).pack()

    Label(tab_settings, text="New Username:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=(30,10))
    Entry(tab_settings, textvariable=new_username_var, width=50).pack(pady=(10,30))

    Label(tab_settings, text="New Password:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
    Entry(tab_settings, textvariable=new_password_var, width=50, show="*").pack()
    Button(tab_settings, text="Save Changes", font=("Arial", 12), command=update_credentials).pack(pady=10)

    notebook.pack(expand=True, fill='both')

    root.mainloop()

# Function to log activities
def log_activity(action, file_type, time_taken, processes):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"\n{timestamp} - {action}\n | File Type: {file_type} |\n | Time Taken: {time_taken}s |\n | Processes: {processes} |\n\n"
    log_display.insert("end", log_message)  # Append to the Text widget
    log_display.yview("end")  # Auto-scroll to the end

# Login Window
login_window = Tk()
login_window.title("User Authentication")
login_window.geometry("400x300")

Label(login_window, text="Username:", font=("Arial", 14)).pack(pady=(70,0))
username = Entry(login_window, width=35)
username.pack(pady=(0,20))

Label(login_window, text="Password:", font=("Arial", 14)).pack()
password = Entry(login_window, width=35, show="*")  # Correct placement of arguments
password.pack()
Button(login_window, text="Login", font=("Arial", 14), command=login).pack(pady=10)
login_window.mainloop()
