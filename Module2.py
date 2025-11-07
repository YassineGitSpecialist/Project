import csv
import psycopg2
from datetime import datetime

CSV_PAD = "berichten.csv"

# Azure databaseconfiguratie
DB_CONFIG = {
    "host": "stationszuil-server.postgres.database.azure.com",
    "dbname": "postgres",
    "user": "postgres",
    "password": "Welkom123",
    "sslmode": "require"
}

def lees_csv():
    with open(CSV_PAD, mode="r", encoding="utf-8") as bestand:
        reader = csv.DictReader(bestand)
        return list(reader)

def schrijf_naar_db(cur, bericht, goedgekeurd, naam_mod, email_mod):
    cur.execute("""
        INSERT INTO berichten_moderatie (
            datum_tijd_bericht, station, naam_reiziger, inhoud_bericht,
            goedgekeurd, datum_tijd_moderatie, naam_moderator, email_moderator
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        bericht["Datum/Tijd"],
        bericht["Station"],
        bericht["Naam"] if bericht["Naam"] else "anoniem",
        bericht["Bericht"],
        goedgekeurd,
        datetime.now(),
        naam_mod,
        email_mod
    ))

def leeg_csv():
    with open(CSV_PAD, mode="w", newline="", encoding="utf-8") as bestand:
        writer = csv.writer(bestand)
        writer.writerow(["Datum/Tijd", "Station", "Naam", "Bericht"])

def start_moderatie():
    berichten = lees_csv()
    if not berichten:
        print("Geen berichten om te modereren.")
        return

    print(f"{len(berichten)} berichten gevonden voor moderatie.\n")

    naam_mod = input("Naam moderator: ").strip()
    email_mod = input("E-mail moderator: ").strip()

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for bericht in berichten:
            print("\nBericht:")
            print(f"- Tijd: {bericht['Datum/Tijd']}")
            print(f"- Station: {bericht['Station']}")
            print(f"- Naam: {bericht['Naam'] or 'anoniem'}")
            print(f"- Inhoud: {bericht['Bericht']}")
            keuze = input("Goedkeuren (j/n)? ").strip().lower()
            goedgekeurd = keuze == "j"
            schrijf_naar_db(cur, bericht, goedgekeurd, naam_mod, email_mod)

        conn.commit()
        cur.close()
        conn.close()
        leeg_csv()
        print("\nAlle berichten zijn beoordeeld en opgeslagen in Azure.")

    except Exception as e:
        print("Fout bij verbinden of schrijven naar de database:", e)

if __name__ == "__main__":
    start_moderatie()