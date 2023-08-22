import pcbnew
import os
import wx
from pcbnew import *
from . import dialog_amf

class Plugin(pcbnew.ActionPlugin):
    def __init__(self):
        self.name = "HQ NextPCB Active Manufacturing"
        self.category = "Manufacturing"
        self.description = "Quote and place order with one button click."
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), 'icon.png')
        self.dark_icon_file_name = os.path.join(
            os.path.dirname(__file__), 'icon.png')

    def Run(self):
        dialog_amf.AmfDialog(None).ShowModal()