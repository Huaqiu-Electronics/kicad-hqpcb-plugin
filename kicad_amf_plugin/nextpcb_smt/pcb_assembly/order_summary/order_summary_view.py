from .ui_order_summary import UiOrderPanel;
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_amf_plugin.icon import GetImagePath
import wx
import wx.dataview as dv
from kicad_amf_plugin.kicad.board_manager import BoardManager

from .order_summary_model import OrderSummaryModel
from kicad_amf_plugin.kicad.helpers import get_valid_footprints


class OrderSummaryView(UiOrderPanel, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager ):
        super().__init__(parent)
        self._board_manager = board_manager
        self.parts_list = []
        
        self.init_ui()
        self.load_Designator()

       
    def load_Designator(self):           
        for fp in get_valid_footprints(self._board_manager.board):
            part = [
                fp.GetReference(),
                fp.GetValue(),
                str(fp.GetFPID().GetLibItemName()),
            ]
            self.list_bom_view.AppendItem(part)
        
    
    def init_ui(self):
        self.list_bom_view.AppendTextColumn(
            _("Designator"),
            0,
            width=80,
            align=wx.ALIGN_CENTER,
            flags=dv.DATAVIEW_COL_RESIZABLE,
        )
        self.list_bom_view.AppendTextColumn(
            _("Value"),
            1,
            width=140,
            align=wx.ALIGN_CENTER,
            flags=dv.DATAVIEW_COL_RESIZABLE,
        )
        self.list_bom_view.AppendTextColumn(
            _("Footprint"),
            2,
            width=-1,
            align=wx.ALIGN_CENTER,
            flags=dv.DATAVIEW_COL_RESIZABLE,
        )


        self.list_price_detail.AppendTextColumn(
            _("Item"),
            0,
            width=140,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.list_price_detail.AppendTextColumn(
            _("Price"),
            1,
            width=-1,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_RIGHT,
        )

        
        self.order_summary_model = OrderSummaryModel()
        self.list_price_detail.AssociateModel(self.order_summary_model)
        
        max_width = 300
        sum = 0
        for i in range(0, self.list_price_detail.GetColumnCount()):
            sum = sum + self.list_price_detail.GetColumn(i).GetWidth()
        max_width = max(max_width, sum)
        sum = 0
        
        self.SetMinSize(wx.Size(max_width + 30, -1))
            
    
    @staticmethod
    def GetLineHeight(parent):
        line = wx.TextCtrl(parent)
        _, height = line.GetSize()
        line.Destroy()
        return height
    
    
    def GetImagePath(self, bitmap_path):
        return GetImagePath(bitmap_path)
    
    
    def set_pcba_count(self, board_count):
        self.pcba_quantity.SetValue(str(board_count))
        
        
