import random
from datetime import datetime, timedelta
from pymongo import MongoClient

class LogistikDatensatz:
    def __init__(self, zeitstempel, lager, bananensorte, menge, lieferant):
        self.zeitstempel = zeitstempel
        self.lager = lager
        self.bananensorte = bananensorte
        self.menge = menge
        self.lieferant = lieferant

    def als_dict(self):
        return {
            "zeitstempel": self.zeitstempel.strftime('%Y-%m-%d %H:%M:%S'),
            "lager": self.lager,
            "bananensorte": self.bananensorte,
            "menge": self.menge,
            "lieferant": self.lieferant
        }

def generiere_logistikdaten(lager_ids, bananensorten, lieferanten, startzeit, intervall, anzahl):
    daten = []
    aktuelle_zeit = startzeit

    for _ in range(anzahl):
        lager = random.choice(lager_ids)
        sorte = random.choice(bananensorten)
        menge = random.randint(50, 200)
        lieferant = random.choice(lieferanten)

        datensatz = LogistikDatensatz(
            zeitstempel=aktuelle_zeit,
            lager=lager,
            bananensorte=sorte,
            menge=menge,
            lieferant=lieferant
        )

        daten.append(datensatz.als_dict())
        aktuelle_zeit += intervall

    return daten

if __name__ == "__main__":
    lager = ['Lager A', 'Lager B', 'Lager C']
    bananensorten = [
        'Cavendish', 'Plantain', 'Red Banana', 'Apple Banana',
        'Blue Java', 'Manzano', 'Burro', 'Goldfinger'
    ]
    lieferanten = ['BananaCorp', 'TropiFruits', 'GreenWorld', 'SunBanana']
    # Erzeuge Daten für 30 Tage, alle 6 Stunden ein Eintrag
    start = datetime.now() - timedelta(days=30)
    intervall = timedelta(hours=6)
    anzahl = 30  # 4 Einträge pro Tag * 30 Tage

    daten = generiere_logistikdaten(lager, bananensorten, lieferanten, start, intervall, anzahl)

    # Verbindung zu MongoDB (Docker-Container)
    client = MongoClient("mongodb://localhost:27017/")
    db = client["supplychain"]
    collection = db["logistikdaten"]

    # Optional: Vorher alte Daten löschen
    collection.delete_many({})

    # Daten einfügen
    collection.insert_many(daten)
    print(f"{len(daten)} Logistikdatensätze erfolgreich in MongoDB gespeichert!")