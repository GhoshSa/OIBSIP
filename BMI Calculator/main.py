import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

def init_db():
    connection = sqlite3.connect("BMI Calculator/data.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS bmi_records (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, weight REAL, height REAL, bmi REAL, date TEXT, FOREIGN KEY(user_id) REFERENCES users(id))")
    connection.commit()
    connection.close()

def add_user_to_db(name):
    try:
        connection = sqlite3.connect("BMI Calculator/data.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_users():
    connection = sqlite3.connect("BMI Calculator/data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM users")
    users = [row[0] for row in cursor.fetchall()]
    connection.close()
    return users

def add_bmi_record(user, weight, height, bmi):
    connection= sqlite3.connect("BMI Calculator/data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE name=?", (user,))
    user_id = cursor.fetchone()[0]
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO bmi_records (user_id, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)", (user_id, weight, height, bmi, date))
    connection.commit()
    connection.close()

def get_bmi_history(user):
    connection= sqlite3.connect("BMI Calculator/data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT weight, height, bmi, date FROM bmi_records WHERE user_id=(SELECT id FROM users WHERE name=?) ORDER BY date ASC", (user,))
    data = cursor.fetchall()
    connection.close()
    return data

def calculate_bmi(weight, height):
    bmi = weight / (height / 100) ** 2
    return round(bmi, 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("650x450")
        self.root.minsize(650, 450)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        title_frame = ttk.Frame(root)
        title_frame.grid(row=0, column=0, pady=20, sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, text="BMI Calculator", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0)

        user_frame = ttk.LabelFrame(root, text="User Management")
        user_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        user_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(user_frame, text="Select User:").grid(row=0, column=0, padx=10, pady=10)
        self.user_var = tk.StringVar()
        self.user_menu = ttk.Combobox(user_frame, textvariable=self.user_var, values=get_users(), state="readonly")
        self.user_menu.grid(row=0, column=1, padx=10, sticky="ew")
        ttk.Button(user_frame, text="Add User", command=self.add_user_gui).grid(row=0, column=2, padx=10)

        input_frame = ttk.LabelFrame(root, text="BMI Calculation")
        input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=10)
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.grid(row=0, column=1, padx=10, sticky="ew")

        ttk.Label(input_frame, text="Height (cm):").grid(row=1, column=0, padx=10, pady=10)
        self.height_entry = ttk.Entry(input_frame)
        self.height_entry.grid(row=1, column=1, padx=10, sticky="ew")

        result_frame = ttk.Frame(root)
        result_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        result_frame.grid_columnconfigure(0, weight=1)

        ttk.Button(result_frame, text="Calculate BMI", command=self.calculate_and_save_bmi).grid(row=0, column=0, pady=15)
        
        self.result_label = ttk.Label(result_frame, text="", font=("Helvetica", 12))
        self.result_label.grid(row=1, column=0, pady=10)

        button_frame = ttk.Frame(root)
        button_frame.grid(row=4, column=0, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="View History", command=self.show_history).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ttk.Button(button_frame, text="Show Graph", command=self.show_graph).grid(row=0, column=1, padx=10, pady=10, sticky="w")

    def add_user_gui(self):
        new_user = tk.simpledialog.askstring("Add User", "Enter new user name:")
        if new_user:
            if add_user_to_db(new_user):
                self.user_menu['values'] = get_users()
                messagebox.showinfo("Success", "User added!")
            else:
                messagebox.showerror("Error", "User already exists!")

    def calculate_and_save_bmi(self):
        try:
            user = self.user_var.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if not user:
                raise ValueError("Select a user!")

            bmi = calculate_bmi(weight, height)
            category = bmi_category(bmi)
            self.result_label.config(text=f"BMI: {bmi} ({category})")

            add_bmi_record(user, weight, height, bmi)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input")

    def show_history(self):
        user = self.user_var.get()
        if not user:
            messagebox.showerror("Error", "Select a user!")
            return
        history = get_bmi_history(user)

        history_window = tk.Toplevel(self.root)
        history_window.title(f"{user} - BMI History")
        columns = ["Weight", "Height", "BMI", "Date"]
        tree = ttk.Treeview(history_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        for row in history:
            tree.insert("", tk.END, values=row)
        tree.pack(fill="both", expand=True)

    def show_graph(self):
        user = self.user_var.get()
        if not user:
            messagebox.showerror("Error", "Select a user!")
            return

        history = get_bmi_history(user)
        if not history:
            messagebox.showerror("Error", "No data to show!")
            return

        # dates = [datetime.datetime.strptime(x[3], "%Y-%m-%d") for x in history]
        # bmi_values = [x[2] for x in history]

        parsed = []
        for _, _, bmi, dates in history:
            date = datetime.datetime.strptime(dates, "%Y-%m-%d")
            parsed.append((date, bmi))

        if not parsed:
            messagebox.showerror("Error", "Date parsing failed.")
            return
        
        parsed.sort(key=lambda t: t[0])
        dates = [d[0] for d in parsed]
        bmi_values = [b[1] for b in parsed]

        fig, ax = plt.subplots()
        ax.plot(dates, bmi_values, marker='o', linestyle='-')
        ax.set_title(f"BMI Trend for {user}")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")

        ax.set_xticks(dates)
        plt.tight_layout()

        graph_window = tk.Toplevel(self.root)
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()