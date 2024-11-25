from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import date

class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.benutzer_drop_down.items = anvil.server.call('get_benutzer')
    self.jugendherberge_drop_down.items = anvil.server.call('get_jugendherbergen')

    self.start_datum_picker.add_event_handler('change', self.button_check_dates_click)
    self.end_datum_picker.add_event_handler('change', self.button_check_dates_click)
    self.jugendherberge_drop_down.add_event_handler('change', self.load_rooms)
    self.benutzer_drop_down.add_event_handler('change', self.load_guests)
    
  def load_guests(self, **event_args):
    guests_data = anvil.server.call('get_all_guests')
    guests_items = []
    for guest in guests_data:
        guests_items.append({'name_gast': guest[0]}) 
    self.repeating_panel_guest.items = guests_items
 
  def load_rooms(self, **event_args):
    selected_benutzer = self.benutzer_drop_down.selected_value
    preiskategorie_data = anvil.server.call('get_preiskategorie_for_zimmer', selected_benutzer)
    preiskategorie_id = int(preiskategorie_data.split("ID ")[-1])
    jid = self.jugendherberge_drop_down.items[self.jugendherberge_drop_down.selected_value - 1][1]
    data = anvil.server.call("get_zimmer_for_jugendherberge", jid, preiskategorie_id)

    new_row = []
    for eintrag in data:
        add = {'zimmerNR': eintrag[0], 'BettAZ': eintrag[1], 'PreisPN': eintrag[2]}
        new_row.append(add)
    self.repeating_panel_1.items = new_row

  def button_check_dates_click(self, **event_args):
    start_date = self.start_datum_picker.date
    end_date = self.end_datum_picker.date
    today = date.today()
    
    if start_date and start_date < today:
        alert("Das Startdatum muss in der Zukunft liegen.")
        self.start_datum_picker.date = None
        return

    if end_date and end_date < today:
        alert("Das Enddatum muss in der Zukunft liegen.")
        self.end_datum_picker.date = None
        return

    if end_date and start_date and end_date <= start_date:
        alert("Das Enddatum muss später als das Startdatum sein.")
        self.end_datum_picker.date = None
    else:
        if start_date and end_date:
            formatted_start_date = start_date.strftime("%Y-%m-%d")
            formatted_end_date = end_date.strftime("%Y-%m-%d")
            print(f"Startdatum: {formatted_start_date}, Enddatum: {formatted_end_date}")
        

  def benutzer_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_benutzer = self.benutzer_drop_down.selected_value
    preiskategorie_name = anvil.server.call('get_preiskategorie_for_benutzer', selected_benutzer)
  
    self.preiskategorie_label.text = preiskategorie_name

  def button_buchen_click(self, **event_args):
  
    if (self.benutzer_drop_down.selected_value is not None and self.jugendherberge_drop_down.selected_value is not None and self.start_datum_picker.date is not None and self.end_datum_picker.date is not None):
      print(self.benutzer_drop_down.selected_value)
      preiskategorie_data = anvil.server.call('get_preiskategorie_for_benutzer', self.benutzer_drop_down.selected_value)
      preiskategorie_number = int(preiskategorie_data.split(":")[1].replace("€", "").strip())
        
      start_date = self.start_datum_picker.date
      end_date = self.end_datum_picker.date
      days = (end_date - start_date).days

      
      for row in self.repeating_panel_1.get_components():
        check_buchung = row.get_components()[0]
        bett_anzahl = row.get_components()[2]
        zimmer_num = row.get_components()[1]
        preis = int(days) * preiskategorie_number
        
        if check_buchung.checked:
          for guest_row in self.repeating_panel_guest.get_components():
            guest_button = guest_row.guest_button  
            guest_name = guest_row.get_components()[1].text

            if guest_button.checked:
              print(f"Gast ausgewählt: {guest_name}")
              zimmer_id = anvil.server.call('get_zimmerid_from_zimmernummer', int(zimmer_num.text))
              if zimmer_id:
                anvil.server.call('add_booking', start_date, end_date, preis, zimmer_id[0], self.benutzer_drop_down.selected_value, guest_name)
                print(f"Buchung hinzugefügt für Zimmernummer {zimmer_num.text} mit ID {zimmer_id[0]}")
                self.start_datum_picker.date = None  
                self.end_datum_picker.date = None  
                self.benutzer_drop_down.selected_value = 1
                self.jugendherberge_drop_down.selected_value = 1
                self.repeating_panel_1.items = []  
              else:
                alert(f"Zimmer-ID für Zimmernummer {zimmer_num} konnte nicht gefunden werden.")
    else:
        alert("Bitte füllen Sie alle erforderlichen Felder aus.", title="Fehlende Informationen")



  
      
    