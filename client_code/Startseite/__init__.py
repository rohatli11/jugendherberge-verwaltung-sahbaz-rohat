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

    print(anvil.server.call("say_hello", "sauron"))
    self.jugendherberge_drop_down.items = anvil.server.call('get_jugendherbergen')
    
  

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    jid = self.jugendherberge_drop_down.items[self.jugendherberge_drop_down.selected_value - 1][1]
    print(jid)
    anvil.server.call("get_zimmer_for_jugendherberge", jid)

      
    