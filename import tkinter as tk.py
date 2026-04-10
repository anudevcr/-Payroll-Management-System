import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database setup+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    designation TEXT,
    hourly_wage REAL,
    hours_worked REAL,
    overtime_hours REAL,
    tax_deductions REAL
)
""")
conn.commit()

# Functions
def add_employee():
    try:
        name = entry_name.get().strip()
        designation = entry_designation.get().strip()
        hourly_wage = float(entry_hourly_wage.get())
        hours_worked = float(entry_hours_worked.get())
        overtime_hours = float(entry_overtime_hours.get())
        tax_deductions = float(entry_tax_deductions.get())

        if not name or not designation:
            raise ValueError("Name and designation cannot be empty")

        cursor.execute("INSERT INTO employees (name, designation, hourly_wage, hours_worked, overtime_hours, tax_deductions) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, designation, hourly_wage, hours_worked, overtime_hours, tax_deductions))
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
    entry_hourly_wage.delete(0, tk.END)
    entry_hours_worked.delete(0, tk.END)
    entry_overtime_hours.delete(0, tk.END)
    entry_tax_deductions.delete(0, tk.END)

def generate_payslip():
    try:
        emp_id = int(entry_emp_id.get())
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        emp = cursor.fetchone()
        if emp:
            # Salary calculation
            basic_salary = emp[3] * emp[4]   # hourly_wage * hours_worked
            overtime_pay = emp[3] * 1.5 * emp[5]   # overtime at 1.5x rate
            gross_salary = basic_salary + overtime_pay
            net_salary = gross_salary - emp[6]

            payslip_window = tk.Toplevel(root)
            payslip_window.title("Payslip")
            payslip_text = f"""
Payslip for {emp[1]} ({emp[2]})
---------------------------------
Hourly Wage   : {emp[3]:.2f}
Hours Worked  : {emp[4]:.2f}
Overtime Hours: {emp[5]:.2f}
Tax Deductions: {emp[6]:.2f}
---------------------------------
Gross Salary  : {gross_salary:.2f}
Net Salary    : {net_salary:.2f}
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

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Designation", "Hourly Wage", "Hours Worked"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Designation", text="Designation")
    tree.heading("Hourly Wage", text="Hourly Wage")
    tree.heading("Hours Worked", text="Hours Worked")

    cursor.execute("SELECT id, name, designation, hourly_wage, hours_worked FROM employees")
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

tk.Label(root, text="Hourly Wage").grid(row=2, column=0)
entry_hourly_wage = tk.Entry(root)
entry_hourly_wage.grid(row=2, column=1)

tk.Label(root, text="Hours Worked").grid(row=3, column=0)
entry_hours_worked = tk.Entry(root)
entry_hours_worked.grid(row=3, column=1)

tk.Label(root, text="Overtime Hours").grid(row=4, column=0)
entry_overtime_hours = tk.Entry(root)
entry_overtime_hours.grid(row=4, column=1)

tk.Label(root, text="Tax Deductions").grid(row=5, column=0)
entry_tax_deductions = tk.Entry(root)
entry_tax_deductions.grid(row=5, column=1)

tk.Button(root, text="Add Employee", command=add_employee).grid(row=6, column=0, columnspan=2, pady=5)

tk.Label(root, text="Employee ID for Payslip").grid(row=7, column=0)
entry_emp_id = tk.Entry(root)
entry_emp_id.grid(row=7, column=1)

tk.Button(root, text="Generate Payslip", command=generate_payslip).grid(row=8, column=0, columnspan=2, pady=5)
tk.Button(root, text="View Employees", command=view_employees).grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()