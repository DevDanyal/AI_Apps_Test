import tkinter as tk
from tkinter import ttk, messagebox

class UnitConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Unit Converter")
        master.geometry("450x250")
        master.resizable(False, False)

        # --- Conversion Data ---
        # Base unit for each category is the first one.
        # Factors are for converting FROM the base unit TO the specified unit.
        self.conversions = {
            "Length": {
                "Meter": 1.0,
                "Kilometer": 0.001,
                "Mile": 0.000621371,
                "Feet": 3.28084,
                "Inches": 39.3701,
            },
            "Weight": {
                "Gram": 1.0,
                "Kilogram": 0.001,
                "Pound": 0.00220462,
                "Ounce": 0.035274,
            },
            "Temperature": {
                "Celsius": 0, "Fahrenheit": 0, "Kelvin": 0 # Handled separately
            }
        }

        self.category_var = tk.StringVar()
        self.from_unit_var = tk.StringVar()
        self.to_unit_var = tk.StringVar()
        self.value_var = tk.DoubleVar()
        self.result_var = tk.StringVar(value="Result...")

        # --- UI Elements ---
        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(expand=True, fill="both")

        # Category Selection
        tk.Label(main_frame, text="Conversion Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.category_menu = ttk.Combobox(main_frame, textvariable=self.category_var, values=list(self.conversions.keys()), state="readonly")
        self.category_menu.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.category_menu.bind("<<ComboboxSelected>>", self.update_units)

        # Value Input
        tk.Label(main_frame, text="Value:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(main_frame, textvariable=self.value_var, font=('arial', 12)).grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # From/To Unit Selection
        tk.Label(main_frame, text="From:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.from_menu = ttk.Combobox(main_frame, textvariable=self.from_unit_var, state="readonly")
        self.from_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(main_frame, text="To:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.to_menu = ttk.Combobox(main_frame, textvariable=self.to_unit_var, state="readonly")
        self.to_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Convert Button
        convert_button = tk.Button(main_frame, text="Convert", command=self.perform_conversion, font=('arial', 12, 'bold'), bg='lightblue')
        convert_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Result Display
        tk.Label(main_frame, textvariable=self.result_var, font=('arial', 14, 'bold')).grid(row=5, column=0, columnspan=3, pady=10)

        # Set default category
        self.category_menu.set("Length")
        self.update_units()

    def update_units(self, event=None):
        """Updates the from/to unit menus based on the selected category."""
        category = self.category_var.get()
        units = list(self.conversions[category].keys())
        self.from_menu['values'] = units
        self.to_menu['values'] = units
        self.from_menu.set(units[0])
        self.to_menu.set(units[1] if len(units) > 1 else units[0])

    def perform_conversion(self):
        """Calculates and displays the converted value."""
        try:
            value = self.value_var.get()
            category = self.category_var.get()
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()

            if not from_unit or not to_unit:
                messagebox.showerror("Error", "Please select units to convert.")
                return

            if category == "Temperature":
                if from_unit == 'Celsius':
                    celsius = value
                elif from_unit == 'Fahrenheit':
                    celsius = (value - 32) * 5/9
                else: # Kelvin
                    celsius = value - 273.15
                
                if to_unit == 'Celsius':
                    result = celsius
                elif to_unit == 'Fahrenheit':
                    result = (celsius * 9/5) + 32
                else: # Kelvin
                    result = celsius + 273.15
            else:
                base_unit = list(self.conversions[category].keys())[0]
                from_factor = self.conversions[category][from_unit]
                base_value = value / from_factor
                to_factor = self.conversions[category][to_unit]
                result = base_value * to_factor
            
            self.result_var.set(f"{result:.4f} {to_unit}")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot convert from this unit.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()
