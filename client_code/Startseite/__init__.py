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

  def load_rooms(self, **event_args):
    # ID der ausgewählten Jugendherberge abrufen
    jid = self.jugendherberge_drop_down.items[self.jugendherberge_drop_down.selected_value - 1][1]
    print(jid)

    rooms = anvil.server.call('get_zimmer_for_jugendherberge', jid)

    self.data_grid.items = [] 
    for room in rooms:
        self.data_grid.items.append({'zimmerNR': room[0], 'BettAZ': room[1]})  

  

  def benutzer_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_benutzer = self.benutzer_drop_down.selected_value
    
    # Call server function to get Preiskategorie for the selected Benutzer
    preiskategorie_name = anvil.server.call('get_preiskategorie_for_benutzer', selected_benutzer)
    
    # Set the label text to the fetched Preiskategorie name
    self.preiskategorie_label.text = preiskategorie_name if preiskategorie_name else "Keine Preiskategorie gefunden"

      
    