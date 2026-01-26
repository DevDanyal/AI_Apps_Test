import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")

        self.data_file = "students.json"
        self.students = self.load_students()

        # --- UI Elements ---
        # Input Frame
        self.input_frame = tk.LabelFrame(root, text="Student Details")
        self.input_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(self.input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.id_entry = tk.Entry(self.input_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(self.input_frame, text="Name:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.name_entry = tk.Entry(self.input_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(self.input_frame, text="Age:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.age_entry = tk.Entry(self.input_frame)
        self.age_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(self.input_frame, text="Grade:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.grade_entry = tk.Entry(self.input_frame)
        self.grade_entry.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        tk.Label(self.input_frame, text="Attendance:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.attendance_entry = tk.Entry(self.input_frame)
        self.attendance_entry.grid(row=1, column=3, padx=5, pady=2, sticky="ew")

        self.input_frame.grid_columnconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(3, weight=1)

        # Buttons Frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5, padx=10)

        self.add_button = tk.Button(self.button_frame, text="Add Student", command=self.add_student)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Update Student", command=self.update_student)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Student", command=self.delete_student)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear Fields", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Treeview for displaying students
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        self.student_tree = ttk.Treeview(self.tree_frame, columns=("ID", "Name", "Age", "Grade", "Attendance"), 
                                         show="headings", yscrollcommand=self.tree_scroll.set)
        self.student_tree.pack(fill="both", expand=True)
        self.tree_scroll.config(command=self.student_tree.yview)

        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Age", text="Age")
        self.student_tree.heading("Grade", text="Grade")
        self.student_tree.heading("Attendance", text="Attendance (Attended/Total)")

        self.student_tree.column("ID", width=50)
        self.student_tree.column("Name", width=150)
        self.student_tree.column("Age", width=50)
        self.student_tree.column("Grade", width=100)
        self.student_tree.column("Attendance", width=150)

        self.student_tree.bind("<<TreeviewSelect>>", self.select_student)

        self.load_treeview_data()

    def load_students(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return []

    def save_students(self):
        with open(self.data_file, "w") as f:
            json.dump(self.students, f, indent=4)

    def load_treeview_data(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for student in self.students:
            attendance_str = f"{student.get('attended_classes', 'N/A')}/{student.get('total_classes', 'N/A')}"
            self.student_tree.insert("", "end", values=(
                student["id"], student["name"], student["age"], student["grade"], attendance_str
            ))

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.attendance_entry.delete(0, tk.END)

    def add_student(self):
        student_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        grade = self.grade_entry.get().strip()
        attendance_input = self.attendance_entry.get().strip()

        if not all([student_id, name, age, grade, attendance_input]):
            messagebox.showerror("Input Error", "All fields are required.")
            return

        if not student_id.isdigit():
            messagebox.showerror("Input Error", "Student ID must be a number.")
            return
        student_id = int(student_id)

        if not age.isdigit() or int(age) <= 0:
            messagebox.showerror("Input Error", "Age must be a positive number.")
            return
        age = int(age)

        try:
            attended, total = map(int, attendance_input.split('/'))
            if attended < 0 or total <= 0 or attended > total:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Attendance must be in 'attended/total' format (e.g., 10/12) with positive numbers.")
            return

        for student in self.students:
            if student["id"] == student_id:
                messagebox.showerror("Duplicate ID", "Student with this ID already exists.")
                return

        new_student = {
            "id": student_id,
            "name": name,
            "age": age,
            "grade": grade,
            "attended_classes": attended,
            "total_classes": total
        }
        self.students.append(new_student)
        self.save_students()
        self.load_treeview_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Student added successfully.")

    def select_student(self, event):
        self.clear_fields()
        selected_item = self.student_tree.focus()
        if not selected_item:
            return
        
        values = self.student_tree.item(selected_item, 'values')
        
        self.id_entry.insert(0, values[0])
        self.name_entry.insert(0, values[1])
        self.age_entry.insert(0, values[2])
        self.grade_entry.insert(0, values[3])
        self.attendance_entry.insert(0, values[4])

    def update_student(self):
        selected_item = self.student_tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a student to update.")
            return

        original_id = int(self.student_tree.item(selected_item, 'values')[0])
        
        student_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        grade = self.grade_entry.get().strip()
        attendance_input = self.attendance_entry.get().strip()

        if not all([student_id, name, age, grade, attendance_input]):
            messagebox.showerror("Input Error", "All fields are required.")
            return
        
        if not student_id.isdigit():
            messagebox.showerror("Input Error", "Student ID must be a number.")
            return
        student_id = int(student_id)

        if not age.isdigit() or int(age) <= 0:
            messagebox.showerror("Input Error", "Age must be a positive number.")
            return
        age = int(age)

        try:
            attended, total = map(int, attendance_input.split('/'))
            if attended < 0 or total <= 0 or attended > total:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Attendance must be in 'attended/total' format (e.g., 10/12) with positive numbers.")
            return

        for i, student in enumerate(self.students):
            if student["id"] == original_id:
                # Check for ID change and if new ID already exists
                if student_id != original_id:
                    for s in self.students:
                        if s["id"] == student_id and s["id"] != original_id:
                            messagebox.showerror("Duplicate ID", "New Student ID already exists.")
                            return

                self.students[i] = {
                    "id": student_id,
                    "name": name,
                    "age": age,
                    "grade": grade,
                    "attended_classes": attended,
                    "total_classes": total
                }
                break
        self.save_students()
        self.load_treeview_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Student updated successfully.")

    def delete_student(self):
        selected_item = self.student_tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a student to delete.")
            return

        student_id_to_delete = int(self.student_tree.item(selected_item, 'values')[0])

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {student_id_to_delete}?"):
            self.students = [s for s in self.students if s["id"] != student_id_to_delete]
            self.save_students()
            self.load_treeview_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Student deleted successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
