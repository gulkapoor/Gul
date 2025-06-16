import os
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import re

# List to store contacts
contacts = []

# File to store contacts
CONTACTS_FILE = "contacts.csv"

def load_contacts():
    """Load contacts from CSV file."""
    global contacts
    contacts = []
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    contacts.append({"name": row['name'], "phone": row['phone']})
        except Exception as e:
            messagebox.showerror("Error", f"Could not load contacts: {str(e)}")
    update_summary()
    view_contacts()

def save_contacts():
    """Save contacts to CSV file."""
    try:
        with open(CONTACTS_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'phone'])
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save contacts: {str(e)}")

def format_phone(phone):
    """Format phone number as (XXX) XXX-XXXX or return original if invalid."""
    digits = re.sub(r'\D', '', phone)  # Remove non-digits
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone  # Return unformatted if not 10 digits

def validate_name(name):
    """Ensure name contains only letters and spaces."""
    return bool(name and re.match(r'^[A-Za-z\s]+$', name))

def add_contact(event=None):
    """Add a contact from input fields."""
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()

    if not validate_name(name):
        messagebox.showwarning("Input Error", "Name must contain only letters and spaces.")
        return
    if not phone.isdigit() or len(phone) < 7:
        messagebox.showwarning("Input Error", "Phone must be digits only and at least 7 digits.")
        return
    if any(contact['name'].lower() == name.lower() for contact in contacts):
        messagebox.showwarning("Input Error", "Contact name already exists.")
        return

    formatted_phone = format_phone(phone)
    contacts.append({"name": name, "phone": formatted_phone})
    save_contacts()
    messagebox.showinfo("Success", f"Contact {name} added!")
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    update_summary()
    view_contacts()

def edit_contact():
    """Edit a contact's phone number by name."""
    name = name_entry.get().strip()
    new_phone = phone_entry.get().strip()

    if not name:
        messagebox.showwarning("Input Error", "Enter a name to edit.")
        return
    if not new_phone.isdigit() or len(new_phone) < 7:
        messagebox.showwarning("Input Error", "New phone must be digits only and at least 7 digits.")
        return

    for contact in contacts:
        if contact['name'].lower() == name.lower():
            contact['phone'] = format_phone(new_phone)
            save_contacts()
            messagebox.showinfo("Success", f"Contact {name}'s phone updated!")
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            update_summary()
            view_contacts()
            return
    messagebox.showwarning("Input Error", "Contact not found.")

def delete_contact(event=None):
    """Delete a contact by name."""
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Enter a name to delete.")
        return

    global contacts
    initial_len = len(contacts)
    contacts = [contact for contact in contacts if contact['name'].lower() != name.lower()]
    if len(contacts) < initial_len:
        save_contacts()
        messagebox.showinfo("Success", f"Contact '{name}' deleted!")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        update_summary()
        view_contacts()
    else:
        messagebox.showwarning("Input Error", "Contact not found.")

def search_contact():
    """Search and highlight contacts by name or phone."""
    query = search_entry.get().strip().lower()
    if not query:
        view_contacts()  # Show all if search is empty
        return

    contact_list.delete(1.0, tk.END)
    matches = [contact for contact in contacts if query in contact['name'].lower() or query in contact['phone'].lower()]
    if not matches:
        contact_list.insert(tk.END, "No matching contacts found.")
    else:
        for contact in matches:
            contact_list.insert(tk.END, f"{contact['name']} | {contact['phone']}\n")
            # Highlight matches
            start = contact_list.search(f"{contact['name']} | {contact['phone']}", 1.0, tk.END)
            end = f"{start}+{len(f'{contact['name']} | {contact['phone']}')}c"
            contact_list.tag_add("highlight", start, end)

def export_contacts():
    """Export contacts to a text file."""
    try:
        with open("exported_contacts.txt", 'w') as file:
            for contact in contacts:
                file.write(f"{contact['name']} | {contact['phone']}\n")
        messagebox.showinfo("Success", "Contacts exported to exported_contacts.txt!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not export contacts: {str(e)}")

def view_contacts():
    """Display all contacts in the text widget."""
    contact_list.delete(1.0, tk.END)
    if not contacts:
        contact_list.insert(tk.END, "No contacts found.")
    else:
        for contact in contacts:
            contact_list.insert(tk.END, f"{contact['name']} | {contact['phone']}\n")
    contact_list.tag_configure("highlight", background="yellow", foreground="black")

def update_summary():
    """Update the summary label with total contacts and last added."""
    total = len(contacts)
    last_added = contacts[-1] if contacts else {"name": "None", "phone": "None"}
    summary_label.config(text=f"Total Contacts: {total}\nLast Added: {last_added['name']} | {last_added['phone']}")

def toggle_theme():
    """Toggle between light and dark themes."""
    global current_theme
    if current_theme == "light":
        root.configure(bg="#2e2e2e")
        input_frame.configure(bg="#2e2e2e")
        button_frame.configure(bg="#2e2e2e")
        title_label.configure(bg="#2e2e2e", fg="white")
        name_label.configure(bg="#2e2e2e", fg="white")
        phone_label.configure(bg="#2e2e2e", fg="white")
        search_label.configure(bg="#2e2e2e", fg="white")
        summary_label.configure(bg="#2e2e2e", fg="white")
        contact_list.configure(bg="#3c3c3c", fg="white", insertbackground="white")
        theme_button.configure(text="Switch to Light Theme", bg="#555555", activebackground="#555555")
        current_theme = "dark"
    else:
        root.configure(bg="#f0f8ff")
        input_frame.configure(bg="#f0f8ff")
        button_frame.configure(bg="#f0f8ff")
        title_label.configure(bg="#f0f8ff", fg="black")
        name_label.configure(bg="#f0f8ff", fg="black")
        phone_label.configure(bg="#f0f8ff", fg="black")
        search_label.configure(bg="#f0f8ff", fg="black")
        summary_label.configure(bg="#f0f8ff", fg="black")
        contact_list.configure(bg="white", fg="black", insertbackground="black")
        theme_button.configure(text="Switch to Dark Theme", bg="#b0bec5", activebackground="#b0bec5")
        current_theme = "light"

def exit_fullscreen(event=None):
    """Allow exiting full screen with Escape key."""
    root.attributes('-fullscreen', False)

# Create the main window
root = tk.Tk()
root.title("PeopleLink")
root.attributes('-fullscreen', True)
root.configure(bg="#f0f8ff")
root.bind("<Escape>", exit_fullscreen)
root.bind("<Return>", add_contact)  # Enter key to add contact
root.bind("<Delete>", delete_contact)  # Delete key to delete contact

# Current theme
current_theme = "light"

# Title label
title_label = tk.Label(root, text="PeopleLink", font=("Arial", 24, "bold"), bg="#f0f8ff")
title_label.pack(pady=20)

# Summary label
summary_label = tk.Label(root, text="Total Contacts: 0\nLast Added: None | None", font=("Arial", 12), bg="#f0f8ff", justify="left")
summary_label.pack(pady=10, anchor="w", padx=40)

# Input frame
input_frame = tk.Frame(root, bg="#f0f8ff")
input_frame.pack(pady=10)

# Name input
name_label = tk.Label(input_frame, text="Name:", font=("Arial", 14), bg="#f0f8ff")
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
name_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10, pady=10)

# Phone input
phone_label = tk.Label(input_frame, text="Phone:", font=("Arial", 14), bg="#f0f8ff")
phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
phone_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
phone_entry.grid(row=1, column=1, padx=10, pady=10)

# Search input
search_label = tk.Label(input_frame, text="Search:", font=("Arial", 14), bg="#f0f8ff")
search_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
search_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
search_entry.grid(row=2, column=1, padx=10, pady=10)
search_entry.bind("<KeyRelease>", lambda event: search_contact())  # Search on key release

# Button frame
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

def create_button(master, text, command, bg_color):
    """Helper function to create styled buttons."""
    return tk.Button(
        master,
        text=text,
        command=command,
        bg=bg_color,
        fg="black",
        font=("Arial", 12, "bold"),
        relief="raised",
        activebackground=bg_color,
        activeforeground="black",
        width=18,
        height=2,
        bd=2
    )

add_btn = create_button(button_frame, "Add Contact", add_contact, "#a5d6a7")
edit_btn = create_button(button_frame, "Edit Contact", edit_contact, "#ffcc80")
delete_btn = create_button(button_frame, "Delete Contact", delete_contact, "#ef9a9a")
view_btn = create_button(button_frame, "View Contacts", view_contacts, "#90caf9")
export_btn = create_button(button_frame, "Export Contacts", export_contacts, "#ce93d8")
theme_button = create_button(button_frame, "Switch to Dark Theme", toggle_theme, "#b0bec5")

add_btn.grid(row=0, column=0, padx=10, pady=5)
edit_btn.grid(row=0, column=1, padx=10, pady=5)
delete_btn.grid(row=0, column=2, padx=10, pady=5)
view_btn.grid(row=0, column=3, padx=10, pady=5)
export_btn.grid(row=0, column=4, padx=10, pady=5)
theme_button.grid(row=0, column=5, padx=10, pady=5)

# Scrollable contact list
contact_frame = tk.Frame(root, bg="#f0f8ff")
contact_frame.pack(fill="both", expand=True, padx=40, pady=20)
contact_list = tk.Text(contact_frame, height=10, width=50, font=("Arial", 14), wrap="word")
contact_list.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(contact_frame, orient="vertical", command=contact_list.yview)
scrollbar.pack(side="right", fill="y")
contact_list.configure(yscrollcommand=scrollbar.set)

# Load contacts at startup
load_contacts()

# Start the main loop
root.mainloop()
