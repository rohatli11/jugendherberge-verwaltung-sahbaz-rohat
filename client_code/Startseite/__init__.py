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


    # Lösung 1
    # items = []
    # for x in anvil.server.call('get_jugendherbergen'):
    #   items.append((x[1], x[0]))
    # self.drop_down_1.items = items
      
    