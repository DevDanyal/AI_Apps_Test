import tkinter as tk
from tkinter import messagebox
import json

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("600x500")

        self.contacts = self.load_contacts()

        # --- UI Elements ---
        # Labels and Entries for contact details
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.phone_label = tk.Label(root, text="Phone:")
        self.phone_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        self.email_label = tk.Label(root, text="Email:")
        self.email_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        self.address_label = tk.Label(root, text="Address:")
        self.address_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons for operations
        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=4, column=0, padx=10, pady=10)

        self.update_button = tk.Button(root, text="Update Contact", command=self.update_contact)
        self.update_button.grid(row=4, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=5, column=0, padx=10, pady=5)

        self.search_label = tk.Label(root, text="Search:")
        self.search_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=6, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_contact)

        # Listbox to display contacts
        self.contacts_listbox = tk.Listbox(root, width=70, height=15)
        self.contacts_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.contacts_listbox.bind("<<ListboxSelect>>", self.select_contact)

        self.populate_listbox()

    def load_contacts(self):
        try:
            with open("contacts.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_contacts(self):
        with open("contacts.json", "w") as f:
            json.dump(self.contacts, f, indent=4)

    def populate_listbox(self, contacts=None):
        self.contacts_listbox.delete(0, tk.END)
        contacts_to_display = contacts if contacts is not None else self.contacts
        for contact in contacts_to_display:
            self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not name or not phone:
            messagebox.showerror("Error", "Name and Phone are required.")
            return

        contact = {"name": name, "phone": phone, "email": email, "address": address}
        self.contacts.append(contact)
        self.save_contacts()
        self.populate_listbox()
        self.clear_entries()
        messagebox.showinfo("Success", "Contact added successfully.")

    def update_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a contact to update.")
            return

        selected_contact_str = self.contacts_listbox.get(selected_index)
        name_to_update = selected_contact_str.split(" - ")[0]
        
        contact_to_update = None
        for i, contact in enumerate(self.contacts):
            if contact['name'] == name_to_update:
                self.contacts[i] = {
                    "name": self.name_entry.get(),
                    "phone": self.phone_entry.get(),
                    "email": self.email_entry.get(),
                    "address": self.address_entry.get()
                }
                break
        
        self.save_contacts()
        self.populate_listbox()
        self.clear_entries()
        messagebox.showinfo("Success", "Contact updated successfully.")

    def delete_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a contact to delete.")
            return

        selected_contact_str = self.contacts_listbox.get(selected_index)
        name_to_delete = selected_contact_str.split(" - ")[0]
        
        self.contacts = [c for c in self.contacts if c['name'] != name_to_delete]
        
        self.save_contacts()
        self.populate_listbox()
        self.clear_entries()
        messagebox.showinfo("Success", "Contact deleted successfully.")

    def search_contact(self, event=None):
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.populate_listbox()
            return

        results = [c for c in self.contacts if search_term in c['name'].lower() or search_term in c['phone']]
        self.populate_listbox(results)

    def select_contact(self, event=None):
        selected_index = self.contacts_listbox.curselection()
        if not selected_index:
            return

        selected_contact_str = self.contacts_listbox.get(selected_index)
        name = selected_contact_str.split(" - ")[0]

        contact = None
        for c in self.contacts:
            if c['name'] == name:
                contact = c
                break

        if contact:
            self.clear_entries()
            self.name_entry.insert(0, contact.get("name", ""))
            self.phone_entry.insert(0, contact.get("phone", ""))
            self.email_entry.insert(0, contact.get("email", ""))
            self.address_entry.insert(0, contact.get("address", ""))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
