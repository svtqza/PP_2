# phonebook.py
import csv
import json
from connect import get_connection


def print_contacts(rows):
    """Print contacts in a readable format."""
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 60)
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]} {row[2] or ''}")
        print(f"Email: {row[3] or ''}")
        print(f"Birthday: {row[4] or ''}")
        print(f"Group: {row[5] or ''}")
        print(f"Phones: {row[6] or ''}")


def get_or_create_group(cur, group_name):
    """Return group id. Create group if it does not exist."""
    if not group_name:
        group_name = "Other"

    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)", (group_name,))
    return cur.fetchone()[0]


def add_contact(first_name, last_name, email, birthday, group_name, phone, phone_type):
    """Add one contact with one phone number."""
    conn = get_connection()
    cur = conn.cursor()

    group_id = get_or_create_group(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (first_name, last_name, email, birthday or None, group_id)
    )

    contact_id = cur.fetchone()[0]

    if phone:
        cur.execute(
            "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, phone_type)
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added successfully.")


def filter_by_group():
    """Show contacts from selected group."""
    group_name = input("Enter group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE LOWER(g.name) = LOWER(%s)
        GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
        ORDER BY c.first_name
        """,
        (group_name,)
    )

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def search_by_email():
    """Search contacts by partial email match."""
    query = input("Enter email part: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE LOWER(c.email) LIKE LOWER(%s)
        GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
        ORDER BY c.first_name
        """,
        (f"%{query}%",)
    )

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def sort_contacts():
    """Sort contacts by name, birthday, or date added."""
    print("Sort by:")
    print("1. name")
    print("2. birthday")
    print("3. date added")

    choice = input("Choose: ")

    allowed = {
        "1": "c.first_name",
        "2": "c.birthday",
        "3": "c.created_at"
    }

    order_by = allowed.get(choice)

    if not order_by:
        print("Invalid choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order_by}
    """

    cur.execute(query)
    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def search_all_fields():
    """Search name, email, group, birthday, and phone using DB function."""
    query = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
    else:
        for row in rows:
            print("-" * 60)
            print(f"ID: {row[0]}")
            print(f"Name: {row[1]} {row[2] or ''}")
            print(f"Email: {row[3] or ''}")
            print(f"Birthday: {row[4] or ''}")
            print(f"Group: {row[5] or ''}")
            print(f"Phone: {row[6] or ''} ({row[7] or ''})")

    cur.close()
    conn.close()


def paginated_navigation():
    """Navigate contacts using next, prev, quit."""
    page_size = 5
    page = 0

    conn = get_connection()
    cur = conn.cursor()

    while True:
        offset = page * page_size

        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (page_size, offset))
        rows = cur.fetchall()

        print(f"\nPage {page + 1}")
        print_contacts(rows)

        command = input("\nnext / prev / quit: ").lower()

        if command == "next":
            if rows:
                page += 1
        elif command == "prev":
            if page > 0:
                page -= 1
        elif command == "quit":
            break
        else:
            print("Unknown command.")

    cur.close()
    conn.close()


def export_to_json():
    """Export all contacts with phones and group to JSON file."""
    filename = input("Enter JSON filename, for example contacts.json: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            c.birthday,
            g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.first_name
        """
    )

    contacts = []

    for contact in cur.fetchall():
        contact_id = contact[0]

        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s",
            (contact_id,)
        )

        phones = [
            {"phone": phone, "type": phone_type}
            for phone, phone_type in cur.fetchall()
        ]

        contacts.append({
            "first_name": contact[1],
            "last_name": contact[2],
            "email": contact[3],
            "birthday": str(contact[4]) if contact[4] else None,
            "group": contact[5],
            "phones": phones
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print(f"Exported to {filename}")


def import_from_json():
    """Import contacts from JSON with duplicate handling."""
    filename = input("Enter JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for contact in contacts:
        first_name = contact["first_name"]

        cur.execute(
            "SELECT id FROM contacts WHERE LOWER(first_name) = LOWER(%s)",
            (first_name,)
        )

        existing = cur.fetchone()

        if existing:
            action = input(f"Duplicate contact {first_name}. skip or overwrite? ").lower()

            if action == "skip":
                continue

            contact_id = existing[0]
            group_id = get_or_create_group(cur, contact.get("group"))

            cur.execute(
                """
                UPDATE contacts
                SET last_name = %s,
                    email = %s,
                    birthday = %s,
                    group_id = %s
                WHERE id = %s
                """,
                (
                    contact.get("last_name"),
                    contact.get("email"),
                    contact.get("birthday"),
                    group_id,
                    contact_id
                )
            )

            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
        else:
            group_id = get_or_create_group(cur, contact.get("group"))

            cur.execute(
                """
                INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    contact.get("first_name"),
                    contact.get("last_name"),
                    contact.get("email"),
                    contact.get("birthday"),
                    group_id
                )
            )

            contact_id = cur.fetchone()[0]

        for phone in contact.get("phones", []):
            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, phone.get("phone"), phone.get("type"))
            )

    conn.commit()
    cur.close()
    conn.close()

    print("JSON import completed.")


def import_from_csv():
    """Import contacts from CSV with new fields."""
    filename = input("Enter CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_or_create_group(cur, row.get("group"))

            cur.execute(
                """
                INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    row.get("first_name"),
                    row.get("last_name"),
                    row.get("email"),
                    row.get("birthday") or None,
                    group_id
                )
            )

            contact_id = cur.fetchone()[0]

            if row.get("phone"):
                cur.execute(
                    "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                    (
                        contact_id,
                        row.get("phone"),
                        row.get("phone_type") or "mobile"
                    )
                )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import completed.")


def call_add_phone():
    """Call stored procedure add_phone."""
    name = input("Contact first name: ")
    phone = input("New phone: ")
    phone_type = input("Type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def call_move_to_group():
    """Call stored procedure move_to_group."""
    name = input("Contact first name: ")
    group_name = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved to group.")


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Add contact")
        print("2. Filter by group")
        print("3. Search by email")
        print("4. Sort contacts")
        print("5. Paginated navigation")
        print("6. Export to JSON")
        print("7. Import from JSON")
        print("8. Import from CSV")
        print("9. Add phone using procedure")
        print("10. Move contact to group using procedure")
        print("11. Search all fields using function")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            first_name = input("First name: ")
            last_name = input("Last name: ")
            email = input("Email: ")
            birthday = input("Birthday YYYY-MM-DD: ")
            group_name = input("Group: ")
            phone = input("Phone: ")
            phone_type = input("Phone type home/work/mobile: ")
            add_contact(first_name, last_name, email, birthday, group_name, phone, phone_type)
        elif choice == "2":
            filter_by_group()
        elif choice == "3":
            search_by_email()
        elif choice == "4":
            sort_contacts()
        elif choice == "5":
            paginated_navigation()
        elif choice == "6":
            export_to_json()
        elif choice == "7":
            import_from_json()
        elif choice == "8":
            import_from_csv()
        elif choice == "9":
            call_add_phone()
        elif choice == "10":
            call_move_to_group()
        elif choice == "11":
            search_all_fields()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
