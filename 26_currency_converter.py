import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x300")
        
        # --- Variables ---
        self.api_key = "YOUR_API_KEY"  # Replace with your actual API key
        self.currencies = self.get_supported_currencies()
        
        # --- UI Elements ---
        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_currency_label = tk.Label(root, text="From:")
        self.from_currency_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.from_currency_combo = ttk.Combobox(root, values=self.currencies)
        self.from_currency_combo.grid(row=1, column=1, padx=10, pady=10)
        self.from_currency_combo.set("USD")

        self.to_currency_label = tk.Label(root, text="To:")
        self.to_currency_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.to_currency_combo = ttk.Combobox(root, values=self.currencies)
        self.to_currency_combo.grid(row=2, column=1, padx=10, pady=10)
        self.to_currency_combo.set("EUR")
        
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def get_supported_currencies(self):
        # For simplicity, we'll use a fixed list of common currencies.
        # A more advanced version could fetch this from the API.
        return ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "PKR"]

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        from_curr = self.from_currency_combo.get()
        to_curr = self.to_currency_combo.get()

        if not from_curr or not to_curr:
            messagebox.showerror("Invalid Selection", "Please select both 'From' and 'To' currencies.")
            return

        if self.api_key == "YOUR_API_KEY":
            messagebox.showwarning("API Key Missing", "Please replace 'YOUR_API_KEY' with your actual API key from exchangerate-api.com.")
            # For demonstration without an API key, let's use fixed rates
            self.result_label.config(text="API Key missing. Using fixed rates for demo.")
            fixed_rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 157.0, "PKR": 278.0}
            if from_curr in fixed_rates and to_curr in fixed_rates:
                result = amount * (fixed_rates[to_curr] / fixed_rates[from_curr])
                self.result_label.config(text=f"{amount} {from_curr} = {result:.2f} {to_curr}")
            else:
                 self.result_label.config(text="Conversion for selected currencies not available in demo.")
            return

        try:
            url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{from_curr}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if data["result"] == "success":
                conversion_rate = data["conversion_rates"][to_curr]
                result = amount * conversion_rate
                self.result_label.config(text=f"{amount} {from_curr} = {result:.2f} {to_curr}")
            else:
                messagebox.showerror("API Error", f"Failed to get exchange rates: {data.get('error-type', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not connect to the API: {e}")
        except KeyError:
            messagebox.showerror("Invalid Currency", "One of the selected currencies is not supported by the API.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
