import json

# File to store contacts
CONTACTS_FILE = 'contacts.json'

# Load contacts from the file
def load_contacts():
    try:
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save contacts to the file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file)

# Add a new contact
def add_contact(contacts):
    name = input("Enter contact name: ")
    phone = input("Enter contact phone number: ")
    email = input("Enter contact email: ")
    contacts.append({'name': name, 'phone': phone, 'email': email})
    save_contacts(contacts)
    print("Contact added successfully!")

# View all contacts
def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
    else:
        for idx, contact in enumerate(contacts, start=1):
            print(f"{idx}. Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}")

# Delete a contact
def delete_contact(contacts):
    view_contacts(contacts)
    try:
        index = int(input("Enter the number of the contact to delete: ")) - 1
        if 0 <= index < len(contacts):
            deleted_contact = contacts.pop(index)
            save_contacts(contacts)
            print(f"Deleted contact: {deleted_contact['name']}")
        else:
            print("Invalid contact number.")
    except ValueError:
        print("Please enter a valid number.")

# Main menu
def main():
    contacts = load_contacts()
    
    while True:
        print("\nContact List")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Delete Contact")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_contacts(contacts)
        elif choice == '3':
            delete_contact(contacts)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
