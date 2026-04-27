import sqlite3

# ------------------------------------------
# 1. Verbindung zur Datenbank herstellen
# ------------------------------------------
# Falls die Datei nicht existiert, wird sie automatisch erstellt
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# ------------------------------------------
# 2. Tabelle zurücksetzen (für reproduzierbare Ergebnisse)
# ------------------------------------------
cursor.execute("DROP TABLE IF EXISTS users")

# ------------------------------------------
# 3. Tabelle erstellen
# ------------------------------------------
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE
)
""")

# ------------------------------------------
# 4. Musterdaten (Seed Data)
# ------------------------------------------
users = [
    ("Max Mustermann", 30, "max@example.com"),
    ("Erika Musterfrau", 25, "erika@example.com"),
    ("John Doe", 40, "john@example.com"),
    ("Anna Schmidt", 35, "anna@example.com"),
    ("Peter Müller", 28, "peter@example.com")
]

cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users)

# Änderungen speichern
conn.commit()
conn.close()

print("✔ Datenbank wurde erstellt und mit Beispieldaten befüllt.")