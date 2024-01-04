import wx
import wx.dataview as dv
from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.kicad.helpers import get_valid_footprints



class FootPrintList(dv.DataViewListCtrl):
    def __init__(self, parent, board_manager: BoardManager ):
        super().__init__(parent)
        self._board_manager = board_manager
        self.load_Designator()
        self.parts_list = []


    def load_Designator(self):           
        for fp in get_valid_footprints(self._board_manager.board):
            part = [
                fp.GetReference(),
                fp.GetValue(),
                str(fp.GetFPID().GetLibItemName()),
            ]
            self.parts_list.append(part)
        
    
        
        
        