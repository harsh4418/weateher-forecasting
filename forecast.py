import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather Forecasting")
        master.geometry("500x500")

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.master)
        self.frame.pack(pady=20)

        self.city_label = ttk.Label(self.frame, text="Enter City:")
        self.city_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.city_name = tk.StringVar()
        self.city_entry = ttk.Entry(self.frame, textvariable=self.city_name)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)

        self.weather_button = ttk.Button(self.frame, text="Get Weather", command=self.get_weather)
        self.weather_button.grid(row=0, column=2, padx=10, pady=10)

        self.weather_label = ttk.Label(self.frame, text="Weather Forecast:", font=("Arial", 14, "bold"))
        self.weather_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.weather_info = tk.Text(self.frame, width=40, height=10)
        self.weather_info.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def get_weather(self):
        city = self.city_name.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        try:
            # Get today's weather
            today_weather = self.get_weather_data(city)

            # Use the trained model to predict tomorrow's weather
            tomorrow_weather = self.predict_future(city)

            # Display weather information
            self.display_weather(today_weather, tomorrow_weather)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def get_weather_data(self, city):
        api_key = "97c1e3b32a5ba24ddb5785a8422014ce"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'temperature': int(data["main"]["temp"] - 273.15),  # Temperature in Celsius
                'weather_main': data["weather"][0]["main"],
                'weather_desc': data["weather"][0]["description"]
            }
            return weather_data
        else:
            raise Exception("Failed to fetch data from the API.")

    def predict_future(self, city):
        # Load the trained model
        model = self.load_model()

        # Get current weather data
        today_weather = self.get_weather_data(city)

        # Predict tomorrow's weather
        X = np.array([[today_weather['temperature']]])
        tomorrow_temperature = model.predict(X)[0]

        # Prepare tomorrow's weather data
        tomorrow_weather = {
            'date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            'temperature': int(tomorrow_temperature),
            'weather_main': "Prediction",
            'weather_desc': "Weather prediction using ML model"
        }
        return tomorrow_weather

    def load_model(self):
        # Load the trained model (you need to implement this method)
        # Example: return RandomForestRegressor()  # or load your saved model
        raise NotImplementedError("You need to implement the load_model method.")

    def display_weather(self, today_weather, tomorrow_weather):
        self.weather_info.delete(1.0, tk.END)
        self.weather_info.insert(tk.END, f"Today's Weather ({today_weather['date']}):\n")
        self.weather_info.insert(tk.END, f"Temperature: {today_weather['temperature']}°C\n")
        self.weather_info.insert(tk.END, f"Weather: {today_weather['weather_main']} - {today_weather['weather_desc']}\n\n")

        self.weather_info.insert(tk.END, f"Tomorrow's Weather ({tomorrow_weather['date']}):\n")
        self.weather_info.insert(tk.END, f"Temperature: {tomorrow_weather['temperature']}°C\n")
        self.weather_info.insert(tk.END, f"Weather: {tomorrow_weather['weather_main']} - {tomorrow_weather['weather_desc']}")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
