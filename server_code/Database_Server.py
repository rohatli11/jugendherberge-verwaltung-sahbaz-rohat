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
def say_hello(name):
  print("Hello, " + name + "!")
  return 42
 
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
def get_zimmer_for_jugendherberge(jid, columns="zimmernummer, bettenanzahl, preis_pro_nacht, ID_jugendh"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {columns} FROM Zimmer WHERE ID_jugendh={jid}"))
  conn.close()
  print(res)
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
            name, preiskategorie = row  # Unpack the tuple
            preiskategorie = int(preiskategorie)
            formatted_results.append(f"{name}: {preiskategorie}€")
        return "\n".join(formatted_results)  # Join results into a single string
    else:
        return "Keine Preiskategorie gefunden"
   