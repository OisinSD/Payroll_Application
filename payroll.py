# Payroll Application 
# This application allows to add users (Saved to JSON), Delete users, Print users(Txt file & console) 
# It creates payroll slips for users, calculating their weekly wages, taking our tax deductions showing gross and net pay

import json
import os

DATA_FILE = "employees.json"

exit_program = False


def load_employees():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except ValueError:
                return []
    return []


def save_employee(employees):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(employees, f, indent=2)


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
    hours_worked = clean_user_input("Enter employee hours worked: ")
    hourly_rate = clean_user_input("Enter employee hourly rate: ")

    new_id = len(employees) + 1
    
    new_employee = {
        "id": new_id,
        "first_name": first_name,
        "second_name": second_name,
        "hourly_rate": hourly_rate,
        "hours_worked_this_week": hours_worked
    }
    
    employees.append(new_employee)
    save_employee(employees)
    
    print(f"Success: {first_name.title()} added with ID #{new_id}!")

def delete_employee(prompt_message):
    # user_input = clean_user_input(prompt_message)
    # employees = load_employees()
    # for emp in employees:
    #     if emp.get('id') == user_input:
    #         employees.remove(emp)

    # save_employee(employees)
    try:
        user_id = int(clean_user_input(prompt_message))
    except ValueError:
        print("Invalid ID. Please enter a numeric employee ID.")
        return

    employees = load_employees()

    updated_employees = []
    for emp in employees:
        if emp.get('id') == user_id:
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
        print(f"""
              ----------------------------------------
              Employee ID:\t\t{emp.get('id')}
              Employee Full Name:\t{emp.get('first_name','').title()} {emp.get('second_name','').title()}
              Employee Hourly Rate:\t{emp.get('hourly_rate')}
              Employee Hours:\t\t{emp.get('hours_worked_this_week')}
              ----------------------------------------
              """)
        

def handle_menu_choice(user_choice):
    match user_choice:
        case "1" | "add employee":
            add_employee()
        case "2" | "delete employee":
            delete_employee("Please Enter Employee ID: ")
        case "3" | "show all employees":
            show_all_employees()
        case "4" | "show user" | "save employee":
            show_user_and_save()
        case "5" | "exit":
            return False
        case _:
            print("Invalid option")
    return True # Keep Program loop running.


def clean_user_input(prompt_message):
    user_input = input(prompt_message).lower().strip()
    return user_input

def main():
    # Use a clearer flag name: `keep_running` is True while the program should continue.
    keep_running = True
    while keep_running:
        main_menu()
        choice = clean_user_input("Enter your choice: ")
        # `handle_menu_choice` returns True to keep running, False to exit.
        keep_running = handle_menu_choice(choice)

if __name__ == "__main__":
    main()