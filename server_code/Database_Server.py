import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#

 
@anvil.server.callable
def get_jugendherbergen():
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT name, ID_jugendh FROM Jugendherberge"))
  conn.close()
  print(res)
  return res

@anvil.server.callable
def get_benutzer():
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT vorname, ID_benutzer FROM Benutzer"))
  conn.close()
  print(res)
  return res

@anvil.server.callable
def get_all_guests():
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = list(cursor.execute("SELECT vorname, ID_gast FROM Gast"))
    conn.close()
    return res

@anvil.server.callable
def get_zimmer_for_jugendherberge(jid, pid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("""
      SELECT zimmernummer, bettenanzahl, Preiskategorie.name 
      FROM Zimmer 
      JOIN Preiskategorie ON Zimmer.ID_preis = Preiskategorie.ID_preis 
      WHERE ID_jugendh = ? AND Zimmer.ID_preis = ? AND gebucht = 0
  """, (jid, pid)))   
  
  return res



@anvil.server.callable
def get_preiskategorie_for_benutzer(bid):
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = list(cursor.execute(f"SELECT Preiskategorie.name, Preiskategorie.preiskategorie FROM Preiskategorie JOIN BenutzerPreiskategorie ON Preiskategorie.ID_preis = BenutzerPreiskategorie.ID_preis WHERE BenutzerPreiskategorie.ID_benutzer = {bid}"))
    conn.close()  
    print(res)
    if res:
        formatted_results = []
        for row in res:
            name, preiskategorie = row 
            preiskategorie = int(preiskategorie)
            formatted_results.append(f"{name}: {preiskategorie}€")
        return "\n".join(formatted_results) 
    else:
        return "Keine Preiskategorie gefunden"


@anvil.server.callable
def get_jugendherbergen_from_id(jid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT name FROM Jugendherberge WHERE ID_jugendh={jid}"))
  conn.close()
  return res


@anvil.server.callable
def get_zimmerid_from_zimmernummer(zimmernummer):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  print(zimmernummer)
  res = list(cursor.execute("SELECT ID_zimmer, zimmernummer FROM Zimmer WHERE zimmernummer = ?", (zimmernummer,)))
  print(res)
  conn.close()
  return res[0]

    

@anvil.server.callable
def get_preiskategorie_for_zimmer(bid):
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    res = list(cursor.execute("""
        SELECT Preiskategorie.name, Preiskategorie.ID_preis 
        FROM Preiskategorie 
        JOIN BenutzerPreiskategorie ON Preiskategorie.ID_preis = BenutzerPreiskategorie.ID_preis 
        WHERE BenutzerPreiskategorie.ID_benutzer = ?
    """, (bid,)))
    
    conn.close()  
    
    if res:
        formatted_results = []
        for row in res:
            name, preis_id = row  
            formatted_results.append(f"{name}: ID {preis_id}")  
        return "\n".join(formatted_results) 
    else:
        return "Keine Preiskategorie gefunden"


@anvil.server.callable
def add_booking(startzeit, endzeit, preis, zimmer_id, benutzer_id, gast_vorname):
    anvil.server.call('handle_guest_booking', benutzer_id, gast_vorname)

    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Buchung (startzeit, endzeit, preis, ID_zimmer, ID_benutzer) 
        VALUES (?, ?, ?, ?, ?)
    ''', (startzeit, endzeit, preis, zimmer_id, benutzer_id))

    cursor.execute('''
        UPDATE Zimmer
        SET gebucht = 1
        WHERE ID_zimmer = ?
    ''', (zimmer_id,))
    conn.commit()
    conn.close()


@anvil.server.callable
def handle_guest_booking(benutzer_id, gast_vorname):
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    cursor.execute("SELECT ID_gast, ID_user FROM Gast WHERE vorname = ?", (gast_vorname,))
    gast = cursor.fetchone()

    if gast:
        gast_id, fk_user = gast
        if fk_user is None:
            cursor.execute("UPDATE Gast SET ID_user = ? WHERE ID_gast = ?", (benutzer_id, gast_id))
            print(f"Gast {gast_vorname} wurde Benutzer-ID {benutzer_id} zugeordnet.")
    else:
        cursor.execute("INSERT INTO Gast (vorname, ID_user) VALUES (?, ?)", (gast_vorname, benutzer_id))
        print(f"Neuer Gast {gast_vorname} mit Benutzer-ID {benutzer_id} wurde hinzugefügt.")
    
    conn.commit()
    conn.close()

