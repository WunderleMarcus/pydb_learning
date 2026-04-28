# ==========================================
# IMPORTS
# ==========================================
import sqlite3
# -> Importiert die SQLite-Bibliothek.
# -> Damit können wir eine lokale Datenbank erstellen und SQL-Befehle ausführen.

# ==========================================
# DATENBANKVERBINDUNG
# ==========================================
conn = sqlite3.connect("example.db")
# -> Erstellt eine Verbindung zur Datenbankdatei "example.db".
# -> Falls die Datei nicht existiert, wird sie automatisch erstellt.

cursor = conn.cursor()
# -> Der Cursor ist unser "Steuerobjekt" für SQL-Befehle.
# -> Über ihn führen wir SELECT, INSERT, UPDATE, DELETE aus.

# ==========================================
# AUSGABE-HILFSFUNKTION
# ==========================================
def print_users(rows):
    # -> Funktion zur formatierten Ausgabe von Benutzer-Daten

    print("\n--- AKTUELLE BENUTZER ---")
    # -> Überschrift für bessere Lesbarkeit in der Konsole

    if not rows:
        # -> Prüft, ob die Liste leer ist
        print("(Keine Daten vorhanden)")
        # -> Falls keine Daten existieren, wird eine Info ausgegeben

    for row in rows:
        # -> Schleife über alle Datensätze (Zeilen aus der DB)

        print(f"ID={row[0]} | Name={row[1]} | Alter={row[2]} | Email={row[3]}")
        # -> Formatiert die Ausgabe:
        #    row[0] = ID
        #    row[1] = Name
        #    row[2] = Alter
        #    row[3] = Email

# ==========================================
# CREATE - DATENSATZ ERSTELLEN
# ==========================================
def create_user(name, age, email):
    # -> Funktion zum Einfügen eines neuen Benutzers

    print("\n[CREATE] Neuer Benutzer wird angelegt...")
    # -> Info für den Nutzer, dass ein INSERT passiert

    try:
        # -> Fehlerbehandlung, falls z. B. Datenbank-Regeln verletzt werden

        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            (name, age, email)
        )
        # -> SQL-Befehl:
        #    Fügt einen neuen Datensatz in die Tabelle "users" ein
        #    ? schützt vor SQL-Injection (sichere Platzhalter)

        conn.commit()
        # -> Speichert die Änderung dauerhaft in der Datenbank

        print("✔ Benutzer erfolgreich erstellt")
        # -> Erfolgsmeldung

    except sqlite3.IntegrityError as e:
        # -> Fängt Fehler ab (z. B. doppelte Einträge)
        print(f"✖ Fehler: {e}")

# ==========================================
# READ - DATEN AUSLESEN
# ==========================================
def read_users():
    # -> Funktion zum Anzeigen aller Benutzer

    print("\n[READ] Alle Benutzer werden geladen...")
    # -> Info-Ausgabe

    cursor.execute("SELECT * FROM users")
    # -> SQL-Befehl:
    #    Holt ALLE Datensätze aus der Tabelle

    rows = cursor.fetchall()
    # -> Speichert alle Ergebnisse in einer Liste

    print_users(rows)
    # -> Übergibt Daten an die Ausgabe-Funktion

# ==========================================
# UPDATE - DATEN ÄNDERN
# ==========================================
def update_user(user_id, new_name, new_email):
    # -> Funktion zum Ändern eines bestehenden Benutzers

    print(f"\n[UPDATE] Benutzer {user_id} wird geändert...")
    # -> Info-Ausgabe mit dynamischer ID

    cursor.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (new_name, new_email, user_id)
    )
    # -> SQL:
    #    Ändert den Namen eines Users mit bestimmter ID
    

    conn.commit()
    # -> Speichert Änderung dauerhaft

    if cursor.rowcount == 0:
        # -> Prüft, ob überhaupt eine Zeile betroffen war
        print("⚠ Kein Datensatz gefunden")
    else:
        print("✔ Benutzer erfolgreich aktualisiert")

# ==========================================
# DELETE - DATEN LÖSCHEN
# ==========================================
def delete_user(user_id):
    # -> Funktion zum Löschen eines Benutzers

    print(f"\n[DELETE] Benutzer {user_id} wird gelöscht...")
    # -> Info-Ausgabe

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    # -> SQL:
    #    Löscht den Datensatz mit passender ID

    conn.commit()
    # -> Speichert Löschung in der Datenbank

    if cursor.rowcount == 0:
        # -> Prüft, ob etwas gelöscht wurde
        print("⚠ Kein Datensatz gefunden")
    else:
        print("✔ Benutzer erfolgreich gelöscht")

# ==========================================
# FILTER MENÜ
# ==========================================
def filter_menu():
    # -> Untermenü speziell für SQL-Filter

    while True:
        # -> Endlosschleife, bis Benutzer zurückgeht

        print("\n========== FILTER MENÜ ==========")
        print("1 - Vergleichsoperatoren")
        print("2 - Logische Operatoren")
        print("3 - LIKE")
        print("4 - IN")
        print("5 - BETWEEN")
        print("6 - IS NULL / IS NOT NULL")
        print("0 - Zurück")

        choice = input("\nAuswahl: ")
        # -> Benutzerentscheidung wird eingelesen

        # ==================================
        # VERGLEICHSOPERATOREN
        # ==================================
        if choice == "1":
            print("\n👉 Vergleichsoperatoren: > < = !=")

            cursor.execute("SELECT * FROM users WHERE age > 25")
            print("\n[Alter > 25]")
            print_users(cursor.fetchall())

            cursor.execute("SELECT * FROM users WHERE age <= 30")
            print("\n[Alter <= 30]")
            print_users(cursor.fetchall())

        # ==================================
        # LOGISCHE OPERATOREN
        # ==================================
        elif choice == "2":
            print("\n👉 Logische Operatoren: AND, OR, NOT")

            cursor.execute("SELECT * FROM users WHERE age > 20 AND age < 30")
            print("\n[Alter 20–30]")
            print_users(cursor.fetchall())

            cursor.execute("SELECT * FROM users WHERE NOT age > 30")
            print("\n[NICHT älter als 30]")
            print_users(cursor.fetchall())

        # ==================================
        # LIKE
        # ==================================
        elif choice == "3":
            print("\n👉 LIKE: Muster-Suche")

            cursor.execute("SELECT * FROM users WHERE name LIKE 'L%'")
            print("\n[Namen beginnen mit L]")
            print_users(cursor.fetchall())

        # ==================================
        # IN
        # ==================================
        elif choice == "4":
            print("\n👉 IN: Mehrere Werte prüfen")

            cursor.execute("SELECT * FROM users WHERE id IN (1,3,5)")
            print("\n[IDs 1,3,5]")
            print_users(cursor.fetchall())

        # ==================================
        # BETWEEN
        # ==================================
        elif choice == "5":
            print("\n👉 BETWEEN: Bereichsfilter")

            cursor.execute("SELECT * FROM users WHERE age BETWEEN 20 AND 30")
            print("\n[Alter 20 bis 30]")
            print_users(cursor.fetchall())

        # ==================================
        # NULL PRÜFUNG
        # ==================================
        elif choice == "6":
            print("\n👉 NULL-Prüfung")

            cursor.execute("SELECT * FROM users WHERE email IS NULL")
            print("\n[Ohne Email]")
            print_users(cursor.fetchall())

            cursor.execute("SELECT * FROM users WHERE email IS NOT NULL")
            print("\n[Mit Email]")
            print_users(cursor.fetchall())

        # ==================================
        # ZURÜCK
        # ==================================
        elif choice == "0":
            break

        else:
            print("⚠ Ungültige Eingabe")

# ==========================================
# DEMO FUNKTION
# ==========================================
def demo():
    # -> Führt alle CRUD-Operationen automatisch aus

    print("\n========== START DEMO ==========")

    read_users()
    # -> Zeigt aktuelle Daten

    create_user("Lisa Beispiel", 22, "lisa@example.com")
    # -> Fügt neuen Benutzer ein

    read_users()
    # -> Zeigt aktualisierte Daten

    update_user(1, "Max Mustermann (Updated)")
    # -> Ändert Benutzer mit ID 1

    read_users()

    delete_user(2)
    # -> Löscht Benutzer mit ID 2

    read_users()

    print("\n========== ENDE DEMO ==========")

# ==========================================
# HAUPTMENÜ
# ==========================================
def menu():
    # -> Zentrale Steuerung des Programms

    while True:
        print("\n========== HAUPTMENÜ ==========")
        print("1 - Alle Benutzer anzeigen")
        print("2 - Benutzer anlegen")
        print("3 - Benutzer ändern")
        print("4 - Benutzer löschen")
        print("5 - Filter-Menü")
        print("6 - Demo")
        print("0 - Beenden")

        choice = input("\nAuswahl: ")

        if choice == "1":
            print("\n👉 READ")
            read_users()

        elif choice == "2":
            print("\n👉 CREATE")
            name = input("Name: ")
            age = int(input("Alter: "))
            email = input("Email: ")
            create_user(name, age, email)

        elif choice == "3":
            print("\n👉 UPDATE")
            user_id = int(input("ID: "))
            new_name = input("Neuer Name: ")
            new_email = input("Email: ")
            update_user(user_id, new_name, new_email)

        elif choice == "4":
            print("\n👉 DELETE")
            user_id = int(input("ID: "))
            delete_user(user_id)

        elif choice == "5":
            print("\n👉 Filter-Menü öffnen")
            filter_menu()

        elif choice == "6":
            demo()

        elif choice == "0":
            print("\nProgramm beendet 👋")
            break

        else:
            print("⚠ Ungültige Eingabe")

# ==========================================
# PROGRAMMSTART
# ==========================================
if __name__ == "__main__":
    # -> Startpunkt des Programms
    menu()
    # -> Öffnet das Hauptmenü

    conn.close()
    # -> Schließt die Datenbankverbindung sauber