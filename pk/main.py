import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import datetime
import io


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

        # Wyświetlenie ikony pogody
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_response = requests.get(icon_url)

        if icon_response.status_code == 200:
            # Konwersja binarnych danych obrazu na obiekt obrazu
            image_data = io.BytesIO(icon_response.content)
            image = Image.open(image_data)
            image = image.resize((50, 50))  # Zmniejszamy obraz
            weather_icon = ImageTk.PhotoImage(image)

            # Ustawienie obrazu w etykiecie
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon  # Zapewnienie, że obraz nie zostanie usunięty przez garbage collector

    else:
        result_label.config(text="Błąd podczas pobierania danych o pogodzie.")


# Funkcja do aktualizowania zegara i daty
def update_clock():
    # Pobranie aktualnej daty i godziny
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    formatted_date = current_time.strftime("%d-%m-%Y")  # Format daty: dzień-miesiąc-rok

    # Aktualizacja tekstu zegara i daty
    clock_label.config(text=f"Godzina: {formatted_time}\nData: {formatted_date}")

    # Wywołanie funkcji co 1000 ms (1 sekunda)
    root.after(1000, update_clock)


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

# Tworzenie etykiety zegara i daty
clock_label = tk.Label(root, font=("Helvetica", 20), justify="center")
clock_label.pack(pady=10)

# Tworzenie etykiety do wyświetlania ikony pogody
icon_label = tk.Label(root)
icon_label.pack()

# Uruchomienie aktualizacji zegara i daty
update_clock()

# Uruchomienie aplikacji
root.mainloop()
