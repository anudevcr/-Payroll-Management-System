import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database setup
conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    designation TEXT,
    basic_salary REAL,
    deductions REAL,
    bonus REAL
)
""")
conn.commit()

# Functions
def add_employee():
    try:
        name = entry_name.get().strip()
        designation = entry_designation.get().strip()
        salary = float(entry_salary.get())
        deductions = float(entry_deductions.get())
        bonus = float(entry_bonus.get())

        if not name or not designation:
            raise ValueError("Name and designation cannot be empty")

        cursor.execute("INSERT INTO employees (name, designation, basic_salary, deductions, bonus) VALUES (?, ?, ?, ?, ?)",
                       (name, designation, salary, deductions, bonus))
        conn.commit()
        messagebox.showinfo("Success", f"Employee '{name}' added successfully!")
        clear_entries()
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_designation.delete(0, tk.END)
    entry_salary.delete(0, tk.END)
    entry_deductions.delete(0, tk.END)
    entry_bonus.delete(0, tk.END)

def generate_payslip():
    try:
        emp_id = int(entry_emp_id.get())
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        emp = cursor.fetchone()
        if emp:
            total_salary = emp[3] - emp[4] + emp[5]
            payslip_window = tk.Toplevel(root)
            payslip_window.title("Payslip")
            payslip_text = f"""
Payslip for {emp[1]} ({emp[2]})
---------------------------------
Basic Salary : {emp[3]:.2f}
Deductions   : {emp[4]:.2f}
Bonus        : {emp[5]:.2f}
---------------------------------
Net Salary   : {total_salary:.2f}
"""
            tk.Label(payslip_window, text=payslip_text, justify="left", font=("Courier", 12)).pack(padx=10, pady=10)
            tk.Button(payslip_window, text="OK", command=payslip_window.destroy).pack(pady=5)
        else:
            messagebox.showerror("Error", "Employee not found!")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric Employee ID")

def view_employees():
    view_window = tk.Toplevel(root)
    view_window.title("Employee List")

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Designation", "Salary"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Designation", text="Designation")
    tree.heading("Salary", text="Basic Salary")

    cursor.execute("SELECT id, name, designation, basic_salary FROM employees")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)

# GUI setup
root = tk.Tk()
root.title("Payroll Management System")

tk.Label(root, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Designation").grid(row=1, column=0)
entry_designation = tk.Entry(root)
entry_designation.grid(row=1, column=1)

tk.Label(root, text="Basic Salary").grid(row=2, column=0)
entry_salary = tk.Entry(root)
entry_salary.grid(row=2, column=1)

tk.Label(root, text="Deductions").grid(row=3, column=0)
entry_deductions = tk.Entry(root)
entry_deductions.grid(row=3, column=1)

tk.Label(root, text="Bonus").grid(row=4, column=0)
entry_bonus = tk.Entry(root)
entry_bonus.grid(row=4, column=1)

tk.Button(root, text="Add Employee", command=add_employee).grid(row=5, column=0, columnspan=2, pady=5)

tk.Label(root, text="Employee ID for Payslip").grid(row=6, column=0)
entry_emp_id = tk.Entry(root)
entry_emp_id.grid(row=6, column=1)

tk.Button(root, text="Generate Payslip", command=generate_payslip).grid(row=7, column=0, columnspan=2, pady=5)
tk.Button(root, text="View Employees", command=view_employees).grid(row=8, column=0, columnspan=2, pady=5)

root.mainloop()
