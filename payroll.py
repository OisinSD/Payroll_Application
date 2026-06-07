# Payroll Application 
# This application allows to add users (Saved to JSON), Delete users, Print users(Txt file & console) 
# It creates payroll slips for users, calculating their weekly wages, taking our tax deductions showing gross and net pay

import json
import os

DATA_FILE = "employees.json"
OVERTIME_RATE = 1.5
PAYE_BAND_ONE = 0.2
PAYE_BAND_TWO = 0.4

exit_program = False


def calculate_yearly_salary(weekly_hours, hourly_rate):
    # Ensure numeric inputs
    try:
        weekly_hours = float(weekly_hours)
        hourly_rate = float(hourly_rate)
    except (TypeError, ValueError):
        return 0.0, 0.0

    if weekly_hours > 40:
        overtime_hours = weekly_hours - 40
        normal_hours = 40
    else:
        overtime_hours = 0.0
        normal_hours = weekly_hours

    weekly_wage = normal_hours * hourly_rate
    yearly_salary = weekly_wage * 52

    # Overtime pay is (overtime hours * hourly rate * overtime multiplier)
    overtime_pay = overtime_hours * hourly_rate * OVERTIME_RATE
    return yearly_salary, overtime_pay


def calculate_PAYE(yearly_salary):
    try:
        yearly = float(yearly_salary)
    except (TypeError, ValueError):
        return 0.0

    if yearly < 44000:
        PAYE = yearly * PAYE_BAND_ONE
    else:
        higher_rate_tax = yearly - 44000
        PAYE = (higher_rate_tax * PAYE_BAND_TWO) + (44000 * PAYE_BAND_ONE)

    return round(PAYE, 2)

def calculate_USC(yearly_salary):
    """Calculate Universal Social Charge (USC) based on yearly salary.

    Bands:
      - 0.5% on first €12,012
      - 2% on the next €16,688
      - 3% on the next €41,344
      - 8% on any amount above €70,044

    Returns the USC amount (float).
    """
    if yearly_salary <= 0:
        return 0.0

    remaining = yearly_salary
    usc = 0.0

    bands = [
        (12012, 0.005),
        (16688, 0.02),
        (41344, 0.03),
        (float('inf'), 0.08),
    ]

    for band_limit, rate in bands:
        if remaining <= 0:
            break
        taxable = min(remaining, band_limit)
        usc += taxable * rate
        remaining -= taxable

    return round(usc, 2)


def calculate_PRSI(yearly_salary):
    """Calculate PRSI based on yearly salary.

    Rule: 4.2% of yearly salary if weekly earnings > €352, otherwise 0.
    Input: yearly_salary (number). Returns PRSI amount (float, rounded).
    """
    try:
        yearly = float(yearly_salary)
    except (TypeError, ValueError):
        return 0.0

    weekly = yearly / 52.0
    if weekly > 352:
        prsi = yearly * 0.042
    else:
        prsi = 0.0

    return round(prsi, 2)


def calculate_gross_pay(yearly_salary):
    """Calculate gross pay (yearly salary before deductions).
    
    Input: yearly_salary (number). Returns gross pay amount (float, rounded).
    """
    try:
        gross = float(yearly_salary)
    except (TypeError, ValueError):
        return 0.0

    return round(gross, 2)


def calculate_net_pay(yearly_salary, paye_paid, usc_paid, prsi_paid):
    """Calculate net pay (gross salary minus all deductions).
    
    Input:
      - yearly_salary (number): Gross yearly salary
      - paye_paid (number): PAYE tax deducted
      - usc_paid (number): USC tax deducted
      - prsi_paid (number): PRSI deducted
    
    Returns: Net pay amount (float, rounded).
    """
    try:
        gross = float(yearly_salary)
        paye = float(paye_paid)
        usc = float(usc_paid)
        prsi = float(prsi_paid)
    except (TypeError, ValueError):
        return 0.0

    net = gross - (paye + usc + prsi)
    return round(net, 2)

def clean_user_input(prompt_message):
    user_input = input(prompt_message).lower().strip()
    return user_input

def load_employees():
    """
    Collect and validate employee details.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except ValueError:
                return []
    return []


def save_employee(employees):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(employees, f, indent=2)
    except ValueError:
        print("Unable to Save Employee Information.")
        return 

def print_employee(employee):
    print(f"""
              ----------------------------------------
              Employee ID:\t\t{employee.get('id')}
              Employee Full Name:\t{employee.get('first_name','').title()} {employee.get('second_name','').title()}
              Employee Hourly Rate:\t{employee.get('hourly_rate')}
              Employee Hours:\t\t{employee.get('hours_worked_this_week')}
              ----------------------------------------
              """)

def main_menu():
    print("""
          =====================
            Main Menu Options
          =====================
          1. Add Employee
          2. Delete Employee
          3. Show All employees
          4. Show Employee & Save
          5. Exit Program
          ====================
          """)
    
def add_employee():
    print("\n--- Add New Employee ---")
    
    # Load existing data
    employees = load_employees()
    first_name = clean_user_input("Enter employee first name: ")
    second_name = clean_user_input("Enter employee second name: ")
    hours_worked_input = clean_user_input("Enter employee hours worked: ")
    hourly_rate_input = clean_user_input("Enter employee hourly rate: ")

    # Convert numeric inputs
    try:
        hours_worked = float(hours_worked_input)
        hourly_rate = float(hourly_rate_input)
    except (TypeError, ValueError):
        print("Invalid numeric input for hours or rate. Employee not added.")
        return

    yearly_salary, overtime_pay = calculate_yearly_salary(hours_worked, hourly_rate)
    total_yearly_salary = yearly_salary + overtime_pay

    PAYE_paid = calculate_PAYE(total_yearly_salary)
    USC_paid = calculate_USC(total_yearly_salary)
    PRSI_paid = calculate_PRSI(total_yearly_salary)
    # Derive new ID from the last employee in the list to avoid duplicates
    if employees:
        try:
            last_id = employees[-1].get('id', 0)
            new_id = int(last_id) + 1
        except (TypeError, ValueError):
            new_id = len(employees) + 1
    else:
        new_id = 1


    new_employee = {
        "id": new_id,
        "first_name": first_name,
        "second_name": second_name,
        "hourly_rate": hourly_rate,
        "hours_worked_this_week": hours_worked,
        "yearly_salary": round(total_yearly_salary, 2),
        "overtime_paid": round(overtime_pay, 2),
        "PAYE_paid": PAYE_paid,
        "USC_paid": USC_paid,
        "PRSI_paid": PRSI_paid
    }
    
    employees.append(new_employee)
    save_employee(employees)
    
    print(f"Success: {first_name.title()} added with ID #{new_id}!")

def delete_employee(prompt_message):
    try:
        user_id = int(clean_user_input(prompt_message))
    except ValueError:
        print("Invalid ID. Please enter a numeric employee ID.")
        return

    employees = load_employees()

    updated_employees = []
    for emp in employees:
        if emp.get('id') != user_id:
            updated_employees.append(emp)

    if len(updated_employees) == len(employees):
        print(f"No employee found with ID {user_id}.")
        return

    save_employee(updated_employees)
    print(f"Employee with ID {user_id} deleted.")

def show_all_employees():
    all_employees = load_employees()
    if not all_employees:
        print("No employees found.")
        return

    for emp in all_employees:
        print_employee(emp)

def show_one_employee():
    all_employees = load_employees()
    try:
        employee_input = int(clean_user_input("Enter Employee ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for emp in all_employees:
        if emp.get('id') == employee_input:
            print_employee(emp)
            return

    print(f"No employee found with ID {employee_input}.")

def handle_menu_choice(user_choice):
    match user_choice:
        case "1" | "add employee":
            add_employee()
        case "2" | "delete employee":
            delete_employee("Please Enter Employee ID: ")
        case "3" | "show all employees":
            show_all_employees()
        case "4" | "show user" | "save employee":
            show_one_employee()
        case "5" | "exit":
            return False
        case _:
            print("Invalid option")
    return True # Keep Program loop running.

def main():
    keep_running = True
    while keep_running:
        main_menu()
        choice = clean_user_input("Enter your choice: ")
        # `handle_menu_choice` returns True to keep running, False to exit.
        keep_running = handle_menu_choice(choice)

if __name__ == "__main__":
    main()