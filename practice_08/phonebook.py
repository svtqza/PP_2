# phonebook.py
import csv
from connect import get_connection


def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_name = row['first_name']
            last_name = row.get('last_name', '')
            phone = row['phone']

            cur.execute(
                "CALL insert_or_update_user(%s, %s, %s)",
                (first_name, last_name, phone)
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
        "CALL insert_or_update_user(%s, %s, %s)",
        (first_name, last_name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("User inserted or updated successfully!")


def search_by_pattern():
    pattern = input("Enter pattern (name, surname, or phone): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    results = cur.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("No matching contacts found.")

    cur.close()
    conn.close()


def get_paginated_contacts():
    limit = int(input("Enter LIMIT: "))
    offset = int(input("Enter OFFSET: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    results = cur.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter username or phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted successfully!")


def insert_many_users():
    n = int(input("How many users do you want to insert? "))

    first_names = []
    last_names = []
    phones = []

    for _ in range(n):
        first_name = input("First name: ")
        last_name = input("Last name: ")
        phone = input("Phone: ")

        first_names.append(first_name)
        last_names.append(last_name)
        phones.append(phone)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many_users(%s, %s, %s, %s)",
        (first_names, last_names, phones, [])
    )

    conn.commit()

    # read returned invalid data
    cur.execute("SELECT %s::text[]", ([],))  # optional placeholder if needed

    cur.close()
    conn.close()
    print("Bulk insert finished.")
    print("Check invalid data directly in SQL if your PostgreSQL driver does not return INOUT automatically.")