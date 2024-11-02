from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.benutzer_drop_down.items = anvil.server.call('get_benutzer')
    self.jugendherberge_drop_down.items = anvil.server.call('get_jugendherbergen')

    self.start_datum_picker.add_event_handler('change', self.button_check_dates_click)
    self.end_datum_picker.add_event_handler('change', self.button_check_dates_click)
    self.jugendherberge_drop_down.add_event_handler('change', self.load_rooms)

  def button_check_dates_click(self, **event_args):
    start_date = self.start_datum_picker.date
    end_date = self.end_datum_picker.date
  
    if end_date and start_date:  
        if end_date <= start_date:
            alert("Das Enddatum muss später als das Startdatum sein.")
            self.end_datum_picker.date = None  
        else:
            formatted_start_date = start_date.strftime("%Y-%m-%d")
            formatted_end_date = end_date.strftime("%Y-%m-%d")
            print(f"Startdatum: {formatted_start_date}, Enddatum: {formatted_end_date}")


  def load_rooms(self, **event_args):
    selected_benutzer = self.benutzer_drop_down.selected_value

    preiskategorie_data = anvil.server.call('get_preiskategorie_for_zimmer', selected_benutzer)
    
    preiskategorie_id = int(preiskategorie_data.split("ID ")[-1])
  
    jid = self.jugendherberge_drop_down.items[self.jugendherberge_drop_down.selected_value - 1][1]
    
    # Call the server to get rooms that match the user's price category
    data = anvil.server.call("get_zimmer_for_jugendherberge", jid, preiskategorie_id)

    new_row = []
        
    for eintrag in data:
        add = {'zimmerNR': eintrag[0], 'BettAZ': eintrag[1], 'PreisPN': eintrag[2]}  # Price is now included
        new_row.append(add)
    
    self.repeating_panel_1.items = new_row


  
  def benutzer_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_benutzer = self.benutzer_drop_down.selected_value
    preiskategorie_name = anvil.server.call('get_preiskategorie_for_benutzer', selected_benutzer)
  
    self.preiskategorie_label.text = preiskategorie_name



  
      
    