from .ui_order_summary import UiOrderPanel;
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_amf_plugin.icon import GetImagePath
import wx
import wx.dataview as dv

from .order_summary_model import OrderSummaryModel


class OrderSummaryView(UiOrderPanel, FormPanelBase):
    def __init__(self,*args, **kw):
        super().__init__(*args, **kw)
        self.init_ui()
    
    def init_ui(self):
        self.list_bom_template.AppendTextColumn(
            _("Designator"),
            0,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            width=140,
            align=wx.ALIGN_CENTER,
        )
        self.list_bom_template.AppendTextColumn(
            _("Qty"),
            1,
            width=140,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.list_bom_template.AppendTextColumn(
            _("MPN"),
            2,
            width=-1,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
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