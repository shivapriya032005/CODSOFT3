import tkinter as tk
from tkinter import messagebox, Scrollbar
import json  # For data persistence using a JSON file
import re

class ContactManager:
    def __init__(self, root):
        """Initialize the main window and the application state."""
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("500x750")
        self.root.config(bg="#e0f7fa")

        # Initialize contacts list, load from file if available
        self.contacts = self.load_contacts_from_file()

        # Create the user interface
        self.create_ui()

    def create_ui(self):
        """Set up the user interface components."""
        # Heading with bold font
        self.heading = tk.Label(self.root, text="Contact Management System", font=("Arial", 20, "bold"), bg="#e0f7fa", fg="#00796b")
        self.heading.pack(pady=20)

        # Listbox Frame for scrolling support
        self.frame = tk.Frame(self.root, bg="#e0f7fa")
        self.frame.pack(pady=10)

        # Scrollbar for Listbox
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox to display contacts
        self.contact_listbox = tk.Listbox(self.frame, font=("Arial", 14), height=10, width=40, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, bg="#ffffff", bd=0, relief=tk.FLAT)
        self.contact_listbox.pack(side=tk.LEFT, padx=10, pady=10)
        self.scrollbar.config(command=self.contact_listbox.yview)

        # Input Frame for adding/updating contact
        self.input_frame = tk.Frame(self.root, bg="#e0f7fa")
        self.input_frame.pack(pady=20)

        # Name input field
        tk.Label(self.input_frame, text="Name:", font=("Arial", 12), bg="#e0f7fa").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Phone input field
        tk.Label(self.input_frame, text="Phone:", font=("Arial", 12), bg="#e0f7fa").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.phone_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=30)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        # Email input field
        tk.Label(self.input_frame, text="Email:", font=("Arial", 12), bg="#e0f7fa").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.email_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=30)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        # Address input field
        tk.Label(self.input_frame, text="Address:", font=("Arial", 12), bg="#e0f7fa").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.address_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=30)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        # Create buttons for different functionalities
        self.create_buttons()

        # Load contacts into the listbox
        self.load_contacts()

    def create_buttons(self):
        """Set up the buttons with icons and styles."""
        button_style = {"font": ("Arial", 12, "bold"), "width": 20, "height": 1, "bd": 0, "relief": tk.RAISED}

        # Add Contact Button
        self.add_btn = tk.Button(self.root, text="➕ Add Contact", **button_style, bg="#4CAF50", fg="white", command=self.add_contact)
        self.add_btn.pack(pady=5)

        # Update Contact Button
        self.update_btn = tk.Button(self.root, text="✏️ Update Contact", **button_style, bg="#ff9800", fg="white", command=self.update_contact)
        self.update_btn.pack(pady=5)

        # Delete Contact Button
        self.delete_btn = tk.Button(self.root, text="🗑️ Delete Contact", **button_style, bg="#f44336", fg="white", command=self.delete_contact)
        self.delete_btn.pack(pady=5)

        # Search Contact Button
        self.search_btn = tk.Button(self.root, text="🔍 Search Contact", **button_style, bg="#03a9f4", fg="white", command=self.search_contact)
        self.search_btn.pack(pady=5)

        # Clear List Button
        self.clear_btn = tk.Button(self.root, text="❌ Clear List", **button_style, bg="#9e9e9e", fg="white", command=self.clear_list)
        self.clear_btn.pack(pady=5)

    def load_contacts(self):
        """Load all contacts into the listbox."""
        self.contact_listbox.delete(0, tk.END)  # Clear the listbox
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def add_contact(self):
        """Add a new contact to the list."""
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if self.validate_contact_input(name, phone) and (email == "" or self.validate_email(email)):
            new_contact = {"name": name, "phone": phone, "email": email or "N/A", "address": address or "N/A"}
            self.contacts.append(new_contact)
            self.save_contacts_to_file()
            messagebox.showinfo("Success", "Contact Added Successfully")
            self.clear_input_fields()
            self.load_contacts()
        else:
            messagebox.showwarning("Error", "Name and Phone Number are required! Email must be valid if provided.")

    def update_contact(self):
        """Update the selected contact."""
        selected = self.contact_listbox.curselection()
        if selected:
            index = selected[0]
            contact = self.contacts[index]

            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            address = self.address_entry.get()

            if self.validate_contact_input(name, phone) and (email == "" or self.validate_email(email)):
                self.contacts[index] = {"name": name, "phone": phone, "email": email or "N/A", "address": address or "N/A"}
                self.save_contacts_to_file()
                messagebox.showinfo("Success", "Contact Updated Successfully")
                self.clear_input_fields()
                self.load_contacts()
            else:
                messagebox.showwarning("Error", "Name and Phone Number are required! Email must be valid if provided.")
        else:
            messagebox.showwarning("Error", "Please select a contact to update!")

    def validate_email(self, email):
        """Validate the email format using regex."""
        if not email:  # If email is empty or None, it is valid
            return True
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def delete_contact(self):
        """Delete the selected contact."""
        selected = self.contact_listbox.curselection()
        if selected:
            index = selected[0]
            del self.contacts[index]  # Delete contact from list
            self.save_contacts_to_file()
            messagebox.showinfo("Success", "Contact Deleted Successfully")
            self.load_contacts()
        else:
            messagebox.showwarning("Error", "Please select a contact to delete!")

    def search_contact(self):
        """Search for a contact by name or phone."""
        query = self.name_entry.get() or self.phone_entry.get()
        results = [contact for contact in self.contacts if query.lower() in contact['name'].lower() or query in contact['phone']]

        if results:
            self.contact_listbox.delete(0, tk.END)
            for contact in results:
                self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")
        else:
            messagebox.showinfo("No Results", "No contacts found for the given query.")
            self.load_contacts()

    def clear_list(self):
        """Clear the contact list from the display (not memory)."""
        self.contact_listbox.delete(0, tk.END)

    def validate_contact_input(self, name, phone):
        """Validate the input for contact name and phone."""
        return bool(name) and bool(phone)

    def save_contacts_to_file(self):
        """Save contacts to a file in JSON format."""
        try:
            with open('contacts.json', 'w') as f:
                json.dump(self.contacts, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save contacts to file: {str(e)}")

    def load_contacts_from_file(self):
        try:
            with open('contacts.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
        # If the file doesn't exist, create an empty contacts file and return an empty list
            with open('contacts.json', 'w') as f:
                json.dump([], f)  # Save an empty list to the file
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error reading contacts file. The file format may be corrupted.")
            return []


    def clear_input_fields(self):
        """Clear input fields after adding or updating contact."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
