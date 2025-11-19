import tkinter as tk
from tkinter import messagebox
import random
import string

def evaluate_strength(password):
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    types_present = sum([has_upper, has_lower, has_digit, has_symbol])
    missing = 4 - types_present

    if missing == 0:
        return "Strong", "green"
    elif missing == 1:
        return "Medium", "orange"
    else:
        return "Weak", "red"

def generate_password():
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number for length.")
        return

    if length < 8:
        messagebox.showwarning("Invalid Length", "Password length must be at least 8.")
        return

    charsets = ""
    if uppercase_var.get(): charsets += string.ascii_uppercase
    if lowercase_var.get(): charsets += string.ascii_lowercase
    if digits_var.get(): charsets += string.digits
    if symbols_var.get(): charsets += string.punctuation

    if not charsets:
        messagebox.showwarning("No Character Set", "Select at least one character type.")
        return

    password = ''.join(random.choice(charsets) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    strength, color = evaluate_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Empty", "No password to copy.")

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x400")
root.config(bg="#f0f0f5")

tk.Label(root, text="Password Generator", font=("Arial", 14, "bold"), bg="#f0f0f5").pack(pady=10)

tk.Label(root, text="Password Length:", bg="#f0f0f5").pack()
length_entry = tk.Entry(root, width=10)
length_entry.pack()

uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()

tk.Checkbutton(root, text="Include Uppercase (A-Z)", variable=uppercase_var, bg="#f0f0f5").pack(anchor='w', padx=30)
tk.Checkbutton(root, text="Include Lowercase (a-z)", variable=lowercase_var, bg="#f0f0f5").pack(anchor='w', padx=30)
tk.Checkbutton(root, text="Include Digits (0-9)", variable=digits_var, bg="#f0f0f5").pack(anchor='w', padx=30)
tk.Checkbutton(root, text="Include Symbols (!@#)", variable=symbols_var, bg="#f0f0f5").pack(anchor='w', padx=30)

tk.Button(root, text="Generate Password", command=generate_password, bg="#4caf50", fg="white", width=20).pack(pady=10)

password_entry = tk.Entry(root, width=35)
password_entry.pack(pady=5)

strength_label = tk.Label(root, text="Strength: ", bg="#f0f0f5")
strength_label.pack()

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196f3", fg="white", width=20).pack(pady=10)

root.mainloop()