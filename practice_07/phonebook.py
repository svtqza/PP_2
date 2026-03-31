# phonebook.py
import csv
from connect import get_connection

def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)",
                (row['first_name'], row['last_name'], row['phone'])
            )
    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted successfully!")

def insert_from_console():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone = input("Enter phone number: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)",
        (first_name, last_name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact added successfully!")

def update_contact():
    phone = input("Enter the phone number of the contact to update: ")
    field = input("Update first_name or phone? ")
    new_value = input(f"Enter new {field}: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE contacts SET {field} = %s WHERE phone = %s", (new_value, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated successfully!")

def query_contacts():
    search_type = input("Search by (name/phone_prefix): ").strip().lower()
    conn = get_connection()
    cur = conn.cursor()

    if search_type == 'name':
        name = input("Enter first name to search: ")
        cur.execute("SELECT first_name, last_name, phone FROM contacts WHERE first_name ILIKE %s", (f"%{name}%",))
    else:
        prefix = input("Enter phone prefix to search: ")
        cur.execute("SELECT first_name, last_name, phone FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))

    results = cur.fetchall()
    if results:
        for r in results:
            print(f"{r[0]} {r[1]}: {r[2]}")
    else:
        print("No contacts found.")
    
    cur.close()
    conn.close()

def delete_contact():
    choice = input("Delete by (username/phone): ").strip().lower()
    conn = get_connection()
    cur = conn.cursor()

    if choice == 'username':
        name = input("Enter first name to delete: ")
        cur.execute("DELETE FROM contacts WHERE first_name = %s", (name,))
    else:
        phone = input("Enter phone number to delete: ")
        cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted successfully!")

def menu():
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            insert_from_csv('contacts.csv')
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()