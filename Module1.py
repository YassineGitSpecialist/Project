import csv
import os
import random
from datetime import datetime


alle_stations = [
"Amsterdam","Den Haag", "Utrecht"
]

#  Pad naar het CSV-bestand
bestandspad = "berichten.csv"

#  Functie om een bericht op te slaan
def sla_bericht_op(bericht, naam, station):
    tijdstip = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not naam.strip():
        naam = "anoniem"
    with open(bestandspad, mode="a", newline="", encoding="utf-8") as bestand:
        schrijver = csv.writer(bestand)
        schrijver.writerow([tijdstip, station, naam, bericht])
    print("\nBericht succesvol opgeslagen.")

#  Command line interface
def start_zuil():
    print("Welkom bij de NS Stationszuil")

    # Kies 3 willekeurige stations en selecteer er één
    gekozen_stations = random.sample(alle_stations, 3)
    station = random.choice(gekozen_stations)

    print(f"\nDeze zuil is gekoppeld aan station: {station}")
    print(f"Gekozen uit: {', '.join(gekozen_stations)}\n")

    naam = input(" Vul je naam in (of laat leeg voor 'anoniem'): ").strip()
    bericht = input("Typ je bericht (max. 140 karakters): ").strip()

    if len(bericht) > 140:
        print("Bericht is te lang. Probeer opnieuw.")
        return

    sla_bericht_op(bericht, naam, station)

# Start het programma
if __name__ == "__main__":
    # Voeg kopregel toe als bestand nog niet bestaat
    if not os.path.exists(bestandspad):
        with open(bestandspad, mode="w", newline="", encoding="utf-8") as bestand:
            schrijver = csv.writer(bestand)
            schrijver.writerow(["Datum/Tijd", "Station", "Naam", "Bericht"])
    start_zuil()
