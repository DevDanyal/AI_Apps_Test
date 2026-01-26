import tkinter as tk
from tkinter import messagebox

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x350")

        # --- Variables ---
        self.weight_unit = tk.StringVar(value="kg")
        self.height_unit = tk.StringVar(value="cm")

        # --- UI Elements ---
        # Weight Input
        self.weight_label = tk.Label(root, text="Weight:")
        self.weight_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=5)

        self.kg_radio = tk.Radiobutton(root, text="kg", variable=self.weight_unit, value="kg", command=self.update_unit_labels)
        self.kg_radio.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.lbs_radio = tk.Radiobutton(root, text="lbs", variable=self.weight_unit, value="lbs", command=self.update_unit_labels)
        self.lbs_radio.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Height Input
        self.height_label = tk.Label(root, text="Height:")
        self.height_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=1, column=1, padx=10, pady=5)

        self.cm_radio = tk.Radiobutton(root, text="cm", variable=self.height_unit, value="cm", command=self.update_unit_labels)
        self.cm_radio.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.inches_radio = tk.Radiobutton(root, text="inches", variable=self.height_unit, value="inches", command=self.update_unit_labels)
        self.inches_radio.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Calculate Button
        self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=4, pady=15)

        # Result Display
        self.bmi_result_label = tk.Label(root, text="Your BMI: ")
        self.bmi_result_label.grid(row=3, column=0, columnspan=4, pady=5)

        self.category_label = tk.Label(root, text="Category: ")
        self.category_label.grid(row=4, column=0, columnspan=4, pady=5)

    def update_unit_labels(self):
        # This function can be expanded if more dynamic label changes are needed.
        # For now, it just ensures the radio buttons are set correctly.
        pass

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Weight and height must be positive values.")
            return

        if self.weight_unit.get() == "lbs":
            weight *= 0.453592  # Convert lbs to kg
        
        if self.height_unit.get() == "inches":
            height *= 2.54  # Convert inches to cm
        
        # Convert height to meters for BMI calculation (cm to m)
        height_m = height / 100

        bmi = weight / (height_m ** 2)
        bmi_category = self.get_bmi_category(bmi)

        self.bmi_result_label.config(text=f"Your BMI: {bmi:.2f}")
        self.category_label.config(text=f"Category: {bmi_category}")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
