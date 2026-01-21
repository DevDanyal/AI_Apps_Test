import tkinter as tk
from tkinter import messagebox

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")
        master.geometry("400x300")
        master.resizable(False, False)

        # --- Placeholder Data ---
        # In a real app, this would come from an API call
        self.weather_data = {
            "New York": {"temperature": "15°C", "condition": "Cloudy", "humidity": "65%"},
            "London": {"temperature": "12°C", "condition": "Rainy", "humidity": "80%"},
            "Tokyo": {"temperature": "22°C", "condition": "Sunny", "humidity": "50%"},
            "Sydney": {"temperature": "25°C", "condition": "Sunny", "humidity": "55%"}
        }

        # --- UI Elements ---

        # Input Frame
        input_frame = tk.Frame(master, pady=10)
        input_frame.pack()

        tk.Label(input_frame, text="Enter City:", font=('arial', 12)).pack(side=tk.LEFT, padx=5)
        self.city_entry = tk.Entry(input_frame, font=('arial', 12), width=15)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        
        self.get_weather_button = tk.Button(input_frame, text="Get Weather", command=self.display_weather, font=('arial', 10, 'bold'), bg='lightblue')
        self.get_weather_button.pack(side=tk.LEFT, padx=5)

        # Weather Display Frame
        self.weather_frame = tk.LabelFrame(master, text="Weather Information", padx=10, pady=10)
        self.weather_frame.pack(padx=10, pady=10, fill="x")

        self.city_label = tk.Label(self.weather_frame, text="", font=('arial', 14, 'bold'))
        self.city_label.pack(pady=5)
        
        self.temp_label = tk.Label(self.weather_frame, text="", font=('arial', 12))
        self.temp_label.pack()

        self.condition_label = tk.Label(self.weather_frame, text="", font=('arial', 12))
        self.condition_label.pack()

        self.humidity_label = tk.Label(self.weather_frame, text="", font=('arial', 12))
        self.humidity_label.pack()


    def display_weather(self):
        """Displays the weather for the entered city using placeholder data."""
        city = self.city_entry.get().strip().title() # Normalize the input city name

        if not city:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return

        if city in self.weather_data:
            data = self.weather_data[city]
            self.city_label.config(text=city)
            self.temp_label.config(text=f"Temperature: {data['temperature']}")
            self.condition_label.config(text=f"Condition: {data['condition']}")
            self.humidity_label.config(text=f"Humidity: {data['humidity']}")
        else:
            self.clear_display()
            messagebox.showerror("Error", f"Weather data not found for '{city}'.\n\nAvailable cities: {', '.join(self.weather_data.keys())}")

    def clear_display(self):
        """Clears the weather display labels."""
        self.city_label.config(text="")
        self.temp_label.config(text="")
        self.condition_label.config(text="")
        self.humidity_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
