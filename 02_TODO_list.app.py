import tkinter as tk
from tkinter import messagebox

class TodoListApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List App")
        master.geometry("400x450")
        master.resizable(False, False)

        self.tasks = []

        # --- UI Elements ---

        # Frame for the entry and add button
        entry_frame = tk.Frame(master)
        entry_frame.pack(pady=10)

        self.task_entry = tk.Entry(entry_frame, width=30, font=('arial', 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(entry_frame, text="Add Task", command=self.add_task, font=('arial', 10, 'bold'), bg='lightblue')
        self.add_button.pack(side=tk.LEFT)

        # Frame for the listbox and scrollbar
        list_frame = tk.Frame(master)
        list_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(list_frame, width=45, height=15, font=('arial', 12), selectbackground='lightgrey')
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Frame for the action buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.complete_button = tk.Button(button_frame, text="Mark Completed", command=self.mark_completed, font=('arial', 10, 'bold'), bg='lightgreen')
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task, font=('arial', 10, 'bold'), bg='orange')
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(button_frame, text="Update Task", command=self.update_task, font=('arial', 10, 'bold'), bg='lightyellow')
        self.update_button.pack(side=tk.LEFT, padx=5)


    def add_task(self):
        """Adds a new task to the list."""
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        """Deletes the selected task."""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def mark_completed(self):
        """Marks the selected task as completed."""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            if not task.endswith(" (Completed)"):
                self.tasks[selected_task_index] = task + " (Completed)"
                self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to mark as completed.")

    def update_task(self):
        """Updates the selected task with new text."""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            new_task = self.task_entry.get()
            if new_task:
                self.tasks[selected_task_index] = new_task
                self.update_listbox()
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", "You must enter a new task text to update.")
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to update.")

    def update_listbox(self):
        """Clears and repopulates the listbox."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)
            if task.endswith(" (Completed)"):
                self.task_listbox.itemconfig(tk.END, {'bg':'lightgreen'})

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
