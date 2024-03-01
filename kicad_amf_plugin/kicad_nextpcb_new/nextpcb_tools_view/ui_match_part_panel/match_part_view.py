import wx
import wx.xrc
import wx.dataview

from .ui_match_part_panel import UiMatchPartPanel
from kicad_amf_plugin.kicad_nextpcb_new.button_id import  ID_MANUAL_MATCH, ID_REMOVE_PART, ID_EXPORT

class MatchPartView(UiMatchPartPanel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)
        
        self.select_part_button.SetDefault()
        self.select_part_button.SetId(ID_MANUAL_MATCH)
        self.remove_part_button.SetDefault()
        self.remove_part_button.SetId(ID_REMOVE_PART)
        self.export_csv.SetId(ID_EXPORT)
        self.export_csv.SetToolTip(wx.ToolTip(_('Export BOM file to the project folder')))
