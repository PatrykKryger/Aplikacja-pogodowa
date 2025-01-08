import tkinter as tk
from tkinter import ttk
import requests

# Funkcja do pobierania pogody
def get_weather():
    city = combo.get()
    api_key = "62aaa211c27926a7c8b71c67b1394826"  # Twój klucz API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pl"

    # Wykonanie zapytania do API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Pobranie informacji o pogodzie
        city_name = combo.get()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Wyświetlenie wyników w oknie
        result_label.config(text=f"Pogoda w {city_name}:\n"
                                 f"Temperatura: {temperature}°C\n"
                                 f"Opis: {description.capitalize()}\n"
                                 f"Wilgotność: {humidity}%\n"
                                 f"Wiatr: {wind_speed} m/s")
    else:
        result_label.config(text="Błąd podczas pobierania danych o pogodzie.")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Aplikacja Pogodowa")

# Tworzenie etykiety z instrukcją
instruction_label = tk.Label(root, text="Podaj nazwę miasta:")
instruction_label.pack()

# Lista dostępnych miast
opcje = ["Gdańsk", "Warszawa", "Kraków"]

# Tworzenie comboboxa
combo = ttk.Combobox(root, values=opcje)
combo.set("Wybierz miasto")  # Ustawiamy domyślną wartość
combo.pack(pady=20)

# Tworzenie przycisku do pobierania danych pogodowych
get_weather_button = tk.Button(root, text="Pobierz pogodę", command=get_weather)
get_weather_button.pack()

# Etykieta do wyświetlania wyników
result_label = tk.Label(root, text="", justify="left")
result_label.pack()

# Uruchomienie aplikacji
root.mainloop()
