import tkinter as tk
import psycopg2
import requests

#  Databaseverbinding
def connect_db():
    return psycopg2.connect(
        host="stationszuil-server.postgres.database.azure.com",
        dbname="postgres",
        user="postgres",
        password="Welkom123",
        sslmode="require"
    )

#Mapping GUI-stationnamen naar database
station_api_namen = {
    "Utrecht Centraal": "Utrecht",
    "Amsterdam": "Amsterdam",
    "Den Haag": "Den Haag"
}

# Berichten ophalen uit berichten_moderatie
def haal_berichten(station_gui_naam):
    station_db_naam = station_api_namen.get(station_gui_naam, station_gui_naam)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT inhoud_bericht, datum_tijd_bericht
        FROM berichten_moderatie
        WHERE goedgekeurd = TRUE AND station = %s
        ORDER BY datum_tijd_bericht DESC
        LIMIT 5
    """, (station_db_naam,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

#  Faciliteiten ophalen uit station_service
def haal_faciliteiten(station_gui_naam):
    station_db_naam = station_api_namen.get(station_gui_naam, station_gui_naam)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT ov_bike, elevator, toilet, park_and_ride
        FROM station_service
        WHERE station_city = %s
    """, (station_db_naam,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

#  Weer ophalen via OpenWeatherMap API
def haal_weer(station_gui_naam):
    api_key = "f3b5ac8c9ca468b3a1b3d89c65dc0797"
    stad = station_api_namen.get(station_gui_naam, "Utrecht")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={stad},NL&appid={api_key}&units=metric&lang=nl"
    try:
        response = requests.get(url)
        data = response.json()
        if "main" in data and "weather" in data:
            temp = data["main"]["temp"]
            omschrijving = data["weather"][0]["description"]
            return f"{temp}°C, {omschrijving}"
        else:
            return "Weerdata onvolledig"
    except Exception as e:
        print("Fout bij ophalen weer:", e)
        return "Weer niet beschikbaar"

#  GUI opbouwen
def start_scherm():
    station_gui_naam = station_var.get()

    # Berichten
    berichten = haal_berichten(station_gui_naam)
    berichten_label.config(text="Laatste berichten:")
    berichten_box.delete("1.0", tk.END)
    if berichten:
        for b in berichten:
            tijd = b[1].strftime('%H:%M') if b[1] else "?"
            berichten_box.insert(tk.END, f"{tijd} - {b[0]}\n")
    else:
        berichten_box.insert(tk.END, "Geen goedgekeurde berichten beschikbaar.\n")

    #  Faciliteiten
    faciliteiten = haal_faciliteiten(station_gui_naam)
    faciliteiten_label.config(text="Faciliteiten:")
    if faciliteiten:
        labels = ["OV-fiets", "Lift", "Toilet", "P+R"]
        beschikbaar = [l for f, l in zip(faciliteiten, labels) if f]
        faciliteiten_box.config(text=", ".join(beschikbaar) if beschikbaar else "Geen")
    else:
        faciliteiten_box.config(text="Geen gegevens")

    #  Weer
    weer = haal_weer(station_gui_naam)
    weer_label.config(text=f"Weer in {station_gui_naam}: {weer}")

# Hoofdvenster
root = tk.Tk()
root.title("Stationshalscherm")

stations = ["Utrecht Centraal", "Amsterdam", "Den Haag"]
station_var = tk.StringVar(value=stations[0])

tk.Label(root, text="Kies een station:").pack()
for s in stations:
    tk.Radiobutton(root, text=s, variable=station_var, value=s).pack()

tk.Button(root, text="Start scherm", command=start_scherm).pack(pady=10)

berichten_label = tk.Label(root, text="")
berichten_label.pack()
berichten_box = tk.Text(root, height=6, width=50)
berichten_box.pack()

faciliteiten_label = tk.Label(root, text="")
faciliteiten_label.pack()
faciliteiten_box = tk.Label(root, text="", fg="blue")
faciliteiten_box.pack()

weer_label = tk.Label(root, text="", fg="green")
weer_label.pack(pady=10)

root.mainloop()